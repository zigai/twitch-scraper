import datetime
import re
from datetime import datetime
from pprint import pp, pprint

import pretty_errors
import requests
from dateutil import parser as dateparser

from twitch_user import TwitchUser
from util import date_to_RFC3339

GAME_IDS = {
    "League of Legends": 21779,
    "Valorant": 516575,
    "Minecraft": 27471,
    "Just Chatting": 509658,
}


class TwitchApiClient:

    def __init__(self, client_id: str, bearer_token: str, verbose: bool = False) -> None:
        self.client_id = client_id
        self.bearer_token = bearer_token
        self.verbose = verbose
        self.headers = {'Authorization': f"Bearer {self.bearer_token}", 'Client-Id': self.client_id}

    def get_channel(self, user_id: str = None, username: str = None):
        if user_id is None and username is None:
            raise ValueError("'user_id' OR 'username' must be specified")
        if user_id and username:
            raise ValueError("Both 'user_id' and 'username' cannot be specified specified")

        url = "https://api.twitch.tv/helix/users"
        querystring = {}
        if user_id is not None:
            querystring["id"] = user_id
        if username is not None:
            querystring["login"] = username
        payload = ""

        response = requests.request(
            "GET",
            url,
            data=payload,
            headers=self.headers,
            params=querystring,
        )
        data = response.json()["data"][0]
        return TwitchUser(
            user_id=data["id"],
            username=data["login"],
            display_name=data["display_name"],
            description=data["description"],
            view_count=data["view_count"],
            profile_image_url=data["profile_image_url"],
            offline_image_url=data["offline_image_url"],
            created_at=dateparser.parse(data["created_at"]),
            broadcaster_type=data["broadcaster_type"],
        )

    def get_game_id(self, name: str):
        if name in GAME_IDS:
            return GAME_IDS[name]

        url = "https://api.twitch.tv/helix/games"
        querystring = {"name": "League of Legends"}
        payload = ""
        response = requests.request(
            "GET",
            url,
            data=payload,
            headers=self.headers,
            params=querystring,
        )
        response = response.json()
        return response["data"]["id"]

    def get_clips(
        self,
        username: str = None,
        game: str = None,
        started_at: datetime = None,
        ended_at: datetime = None,
    ):
        started_at = date_to_RFC3339(started_at)
        ended_at = date_to_RFC3339(ended_at)

        if username is not None:
            username = self.get_channel(username=username).user_id
        if game is not None:
            game = self.get_game_id(game)

        def _req(
            broadcaster_id: str = None,
            game_id: str = None,
            started_at: str = None,
            ended_at: str = None,
            after: str = None,
            before: str = None,
        ):

            url = "https://api.twitch.tv/helix/clips"
            payload = ""
            querystring = {}
            if broadcaster_id is not None:
                querystring["broadcaster_id"] = broadcaster_id
            if game_id is not None:
                querystring["game_id"] = game_id
            if started_at is not None:
                querystring["started_at"] = started_at
            if ended_at is not None:
                querystring["ended_at"] = ended_at
            if after is not None:
                querystring["after"] = after
            if before is not None:
                querystring["before"] = before

            response = requests.request(
                "GET",
                url,
                data=payload,
                headers=self.headers,
                params=querystring,
            )

            return response.json()

        assert type(started_at) is str
        assert type(ended_at) is str
        data = _req(broadcaster_id=username, game_id=game, started_at=started_at, ended_at=ended_at)
        try:
            next_page_token = data["pagination"]["cursor"]
        except:
            ...
        while data.get("pagination")

from secrets import *


def main():
    client = TwitchApiClient(client_id=client_id, bearer_token=bearer)
    u = client.get_channel(username="jankos")
    pprint(u.dict)


if __name__ == '__main__':
    main()
