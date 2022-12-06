from stdl.dt import datetime, fmt_datetime, time
from stdl.fs import json_dump, os
from stdl.str_u import FG, colored

from twitch_scraper.client import TwitchApiClient


class TwitchScraper(TwitchApiClient):
    def __init__(
        self,
        save_dir: str,
        client_id: str,
        bearer: str,
        verbose: bool = True,
        delay: float = 5,
        cache: str | None = None,
    ) -> None:
        super().__init__(client_id, bearer, cache, verbose)
        self.save_directory = save_dir
        self.delay_seconds = delay

    def log(self, text: str):
        if self.verbose:
            print(text)

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
            username (str): username of the streamer
            game (str): name of the game
            started_at (datetime.datetime): starting date/time
            ended_at (datetime.datetime): ending date/time
            limit (int): number of clips to
        Returns:
            None
        """
        clips = self.get_clips(username, game, started_at, ended_at, limit)
        for i in clips:
            self.log(
                (
                    f"{colored('Downloading',FG.LIGHT_GREEN)} "
                    f"'{colored(i.title,FG.BOLD)}'"
                    f" ({colored(i.url,FG.LIGHT_BLUE)})"
                )
            )
            i.download(directory=self.save_directory, progressbar=self.verbose)
            if self.verbose:
                self.log("_" * 64)
            time.sleep(self.delay_seconds)

    def profiles(self, usernames: list[str]):
        """
        Scrape Twitch.tv user profiles

        Args:
            usernames: profiles to scrape
        Returns:
            None
        """
        data = []
        for i in usernames:
            user = self.get_user(username=i)
            self.log(f"Getting data for user '{colored(i, FG.LIGHT_BLUE)}' ...")
            if user is None:
                self.log(colored(f"User '{i}' not found", FG.RED))
            else:
                data.append(user.dict)
                time.sleep(self.delay_seconds)
        today = fmt_datetime(t_sep=" - ")
        filename = f"users.{today}.json"
        path = f"{self.save_directory}{os.sep}{filename}"
        json_dump(data, path=path)
