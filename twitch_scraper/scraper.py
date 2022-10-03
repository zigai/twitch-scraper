import os
import time
from datetime import datetime

from stdl.datetime_u import fmt_datetime
from stdl.fs import json_dump
from stdl.str_u import FG, colored

from twitch_scraper.client import TwitchApiClient


class TwitchScraper(TwitchApiClient):
    def __init__(
        self,
        save_directory: str,
        client_id: str,
        bearer_token: str,
        verbose: bool = True,
        delay_seconds: float = 5,
    ) -> None:
        super().__init__(client_id, bearer_token, "./cache.json", verbose)
        self.save_directory = save_directory
        self.delay_seconds = delay_seconds

    def clips(
        self,
        username: str | None = None,
        game: str | None = None,
        started_at: datetime | None = None,
        ended_at: datetime | None = None,
        limit: int = 1000,
    ):
        """
        Scrape Twitch.tv clips

        Args:
            username (str): username of the broadcaster for whom clips are returned
            game (str): name of the game for which clips are returned
            started_at (datetime.datetime): starting date/time for returned clips
            ended_at (datetime.datetime): ending date/time for returned clips
            limit (int): how many clips to return
        Returns:
            None
        """
        clips = self.get_clips(username, game, started_at, ended_at, limit)
        for i in clips:
            if self.verbose:
                print(
                    (
                        f"{colored('Downloading',FG.LIGHT_GREEN)} "
                        f"'{colored(i.title,FG.BOLD)}'"
                        f" ({colored(i.url,FG.LIGHT_BLUE)})"
                    )
                )
            i.download(directory=self.save_directory, progressbar=self.verbose)
            if self.verbose:
                print("_" * 64)
            time.sleep(self.delay_seconds)

    def profiles(self, usernames: list[str]):
        """
        Scrape Twitch.tv user profiles

        Args:
            usernames: usernames of the profiles to scrape
        Returns:
            None
        """
        data = []
        for i in usernames:
            user = self.get_channel(username=i)
            username_str = colored(i, FG.LIGHT_BLUE)
            if self.verbose:
                print(f"Getting data for user '{username_str}' ...")
            if user is None:
                if self.verbose:
                    print(colored(f"User '{i}' not found", FG.RED))
            else:
                data.append(user.dict)
                time.sleep(self.delay_seconds)
        today = fmt_datetime(t_sep=" - ")
        filename = f"users.{today}.json"
        path = f"{self.save_directory}{os.sep}{filename}"
        json_dump(data, path=path)
