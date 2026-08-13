from __future__ import annotations

from typing import Any, TypeAlias

import requests
from stdl import fs
from stdl.dt import datetime, parse_datetime_str

from twitch_scraper.clip import TwitchClip
from twitch_scraper.user import TwitchUser
from twitch_scraper.util import JsonValue, date_to_rfc3339

CacheData: TypeAlias = dict[str, JsonValue]
RequestParam: TypeAlias = str | int | None


class TwitchAuthError(Exception):
    def __init__(self, message: str = "") -> None:
        self.message = message
        super().__init__(self.message)


class TwitchApiClient:
    API_URL = "https://api.twitch.tv/helix/"

    def __init__(
        self,
        client_id: str,
        bearer_token: str,
        cache_path: str | None = None,
        *,
        verbose: bool = False,
    ) -> None:
        self.client_id = client_id
        self.bearer_token = bearer_token
        self.verbose = verbose
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Client-Id": self.client_id,
        }
        self.cache_path = cache_path
        self.cache = self._cache_load()

    def get(self, url: str, params: dict[str, RequestParam]) -> dict[str, Any]:
        params = {k: v for k, v in params.items() if v is not None}
        response = requests.request(
            "GET",
            self.API_URL + url,
            data="",
            headers=self.headers,
            params=params,
            timeout=30,
        )
        data = response.json()
        self._validate_response(data)

        return data

    def save_cache(self) -> None:
        if self.cache_path is not None:
            fs.json_dump(self.cache, self.cache_path)

    def get_user(
        self, user_id: str | None = None, username: str | None = None
    ) -> TwitchUser | None:
        if user_id is None and username is None:
            raise ValueError("'user_id' or 'username' must be specified")
        if user_id and username:
            raise ValueError("Both 'user_id' and 'username' cannot be specified")

        params: dict[str, RequestParam] = {}
        params["id"] = user_id
        params["login"] = username

        response = self.get("users", params)
        data = response["data"][0]
        if data is None:
            return None

        return TwitchUser(
            user_id=data["id"],
            username=data["login"],
            display_name=data["display_name"],
            description=data["description"],
            view_count=data["view_count"],
            profile_image_url=data["profile_image_url"],
            offline_image_url=data["offline_image_url"],
            created_at=parse_datetime_str(data["created_at"]),
            broadcaster_type=data["broadcaster_type"],
        )

    def get_game_id(self, name: str) -> str:
        if game_id := self._cache_get("game_id", name):
            return game_id

        response = self.get("games", {"name": name})
        game_id = response["data"][0]["id"]
        self._cache_put("game_id", name, game_id)

        return game_id

    def get_clips(
        self,
        username: str | None = None,
        game: str | None = None,
        started_at: datetime | None = None,
        ended_at: datetime | None = None,
        limit: int = 1000,
    ) -> list[TwitchClip]:
        # This seems to be a lie
        # if limit > 1000:
        #    raise ValueError("Cannot return more than 1000 clips")

        def __get_clips(params: dict[str, RequestParam]) -> dict[str, Any]:
            params["first"] = 100
            return self.get("clips", params)

        started_at_param: str | None = None
        if started_at is not None:
            started_at_param = date_to_rfc3339(started_at)

        ended_at_param: str | None = None
        if ended_at is not None:
            ended_at_param = date_to_rfc3339(ended_at)

        user_id: str | None = None
        if username is not None:
            user = self.get_user(username=username)
            user_id = None if user is None else user.user_id

        if game is not None:
            game = self.get_game_id(game)

        clips = []
        data = __get_clips(
            {
                "broadcaster_id": user_id,
                "game_id": game,
                "started_at": started_at_param,
                "ended_at": ended_at_param,
            }
        )
        clips.extend([TwitchClip.from_json(i) for i in _response_items(data)])

        next_page_token = _next_page_token(data)

        while next_page_token:
            data = __get_clips(
                {
                    "broadcaster_id": user_id,
                    "game_id": game,
                    "started_at": started_at_param,
                    "ended_at": ended_at_param,
                    "after": next_page_token,
                }
            )
            clips.extend([TwitchClip.from_json(i) for i in _response_items(data)])
            if len(clips) >= limit:
                break

            next_page_token = _next_page_token(data)

        return clips

    def _cache_load(self) -> CacheData:
        if self.cache_path is not None:
            if fs.File(self.cache_path).exists:
                data = fs.json_load(self.cache_path)
                if isinstance(data, dict):
                    return _validate_cache_data(data)
            else:
                print(f"No cache found at '{self.cache_path}'")
                return _get_empty_cache()

        return _get_empty_cache()

    def _cache_get(self, category: str, key: str) -> str | None:
        entries = self.cache.get(category)
        if not isinstance(entries, dict):
            return None

        value = entries.get(key)
        if isinstance(value, str):
            return value

        return None

    def _cache_put(self, category: str, key: str, val: str) -> None:
        entries = self.cache.get(category)
        if not isinstance(entries, dict):
            entries = {}
            self.cache[category] = entries

        entries[key] = val

    def _validate_response(self, response: dict[str, Any]) -> None:
        if response.get("error"):
            raise TwitchAuthError(str(response))


def _response_items(response: dict[str, Any]) -> list[dict[str, Any]]:
    data = response.get("data")
    if not isinstance(data, list):
        return []

    return [item for item in data if isinstance(item, dict)]


def _next_page_token(response: dict[str, Any]) -> str | None:
    pagination = response.get("pagination")
    if not isinstance(pagination, dict):
        return None

    cursor = pagination.get("cursor")
    if isinstance(cursor, str) and cursor:
        return cursor

    return None


def _validate_cache_data(data: dict[str, JsonValue]) -> CacheData:
    cache: CacheData = {}
    for category, entries in data.items():
        if not isinstance(entries, dict):
            continue

        validated: dict[str, JsonValue] = {
            key: value for key, value in entries.items() if isinstance(value, str)
        }

        cache[category] = validated

    return cache


def _get_empty_cache() -> CacheData:
    return {"game_id": {}, "users": {}, "clips": {}}
