from typing import Any

import requests
from stdl import fs
from stdl.dt import datetime, parse_datetime_str

from twitch_scraper.clip import TwitchClip
from twitch_scraper.user import TwitchUser
from twitch_scraper.util import date_to_rfc3339


class TwitchAuthError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class TwitchApiClient:
    API_URL = "https://api.twitch.tv/helix/"

    def __init__(
        self,
        client_id: str,
        bearer_token: str,
        cache_path: str | None = None,
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

    def __get_empty_cache(self) -> dict[str, dict[str, Any]]:
        return {"game_id": {}, "users": {}, "clips": {}}

    def _cache_load(self):
        if self.cache_path is not None:
            if fs.File(self.cache_path).exists:
                return fs.json_load(self.cache_path)
            else:
                print(f"No cache found at '{self.cache_path}'")
                return self.__get_empty_cache()
        return self.__get_empty_cache()

    def _cache_get(self, category: str, key: str):
        try:
            return self.cache[category][key]  # type:ignore
        except KeyError:
            return None

    def _cache_put(self, category: str, key: str, val):
        self.cache[category][key] = val  # type:ignore

    def get(self, url: str, params: dict):
        params = {k: v for k, v in params.items() if v is not None}
        response = requests.request(
            "GET",
            self.API_URL + url,
            data="",
            headers=self.headers,
            params=params,
        )
        data = response.json()
        self._validate_response(data)
        return data

    def save_cache(self):
        if self.cache_path is not None:
            fs.json_dump(self.cache, self.cache_path)

    def _validate_response(self, response: dict):
        if response.get("error"):
            raise TwitchAuthError(str(response))

    def get_user(self, user_id: str | None = None, username: str | None = None):
        if user_id is None and username is None:
            raise ValueError("'user_id' or 'username' must be specified")
        if user_id and username:
            raise ValueError(
                "Both 'user_id' and 'username' cannot be specified specified"
            )

        params = {}
        params["id"] = user_id
        params["login"] = username

        response = self.get("users", params)
        data = response["data"][0]
        if data is None:
            return None

        user = TwitchUser(
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
        return user

    def get_game_id(self, name: str):
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

        def __get_clips(
            broadcaster_id: str | None = None,
            game_id: str | None = None,
            started_at: str | None = None,
            ended_at: str | None = None,
            after: str | None = None,
            before: str | None = None,
        ):
            params = {k: v for k, v in locals().items() if v is not None}
            params["first"] = 100
            clips = self.get("clips", params)
            return clips

        if started_at is not None:
            started_at = date_to_rfc3339(started_at)  # type:ignore
        if ended_at is not None:
            ended_at = date_to_rfc3339(ended_at)  # type:ignore
        if username is not None:
            user = self.get_user(username=username)
            if user is None:
                user_id = None
            else:
                user_id = user.user_id
        if game is not None:
            game = self.get_game_id(game)

        clips = []
        data = __get_clips(
            broadcaster_id=user_id,  # type:ignore
            game_id=game,
            started_at=started_at,  # type:ignore
            ended_at=ended_at,  # type:ignore
        )
        clips.extend([TwitchClip.from_json(i) for i in data["data"]])

        try:
            next_page_token = data["pagination"]["cursor"]
        except:
            next_page_token = None

        while next_page_token:
            data = __get_clips(
                broadcaster_id=username,
                game_id=game,
                started_at=started_at,  # type:ignore
                ended_at=ended_at,  # type:ignore
                after=next_page_token,
            )
            clips.extend([TwitchClip.from_json(i) for i in data["data"]])
            if len(clips) >= limit:
                break
            try:
                next_page_token = data["pagination"]["cursor"]
            except:
                next_page_token = None

        return clips
