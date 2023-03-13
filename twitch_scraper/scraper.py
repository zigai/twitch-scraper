from os import get_terminal_size

from stdl.dt import datetime, fmt_datetime, time
from stdl.fs import json_dump, os
from stdl.str_u import FG, colored

from twitch_scraper.client import TwitchApiClient


class TwitchScraper(TwitchApiClient):
    """
    Twitch.tv scraper

    Args:
        save_dir (str): Save directory
        client_id (str): Twitch.tv client ID
        bearer (str): Twitch.tv bearer token
        verbose (bool): Print status messages
        delay (float): Delay between requests (seconds)
        cache (str): Path to cache file
    """

    def __init__(
        self,
        save_dir: str,
        client_id: str,
        bearer: str,
        verbose: bool = True,
        delay: float = 0.5,
        cache: str | None = None,
    ) -> None:
        """
        Twitch.tv scraper

        Args:
            save_dir (str): directory to save files
            client_id (str): Twitch.tv client ID
            bearer (str): Twitch.tv bearer token
            verbose (bool): Print status messages
            delay (float): Delay between requests (seconds)
            cache (str): Path to cache file
        """
        super().__init__(client_id, bearer, cache, verbose)
        self.save_directory = save_dir
        self.delay_seconds = delay

    def _log(self, text: str):
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
            username (str): Username of the streamer
            game (str): Mame of the game
            started_at (datetime.datetime): Starting date/time
            ended_at (datetime.datetime): Ending date/time
            limit (int): Number of clips to scrape
        Returns:
            None
        """
        clips = self.get_clips(username, game, started_at, ended_at, limit)
        for i in clips:
            self.log(
                (
                    f"{colored('Downloading',FG.LIGHT_GREEN)} "
                    f"'{colored(clip.title,FG.BOLD)}'"
                    f" ({colored(clip.url,FG.LIGHT_BLUE)})"
                )
            )
            i.download(directory=self.save_directory, progressbar=self.verbose)
            self.log("_" * get_terminal_size().columns)
            time.sleep(self.delay_seconds)

    def profiles(self, usernames: list[str]):
        """
        Scrape Twitch.tv user profiles

        Args:
            usernames: Profiles to scrape
        Returns:
            None
        """
        data = []
        for username in usernames:
            user = self.get_user(username=username)
            self._log(f"Getting data for user '{colored(username, FG.LIGHT_BLUE)}' ...")
            if user is None:
                self._log(colored(f"User '{username}' not found", FG.RED))
            else:
                data.append(user.dict)
                time.sleep(self.delay_seconds)
                self._log("_" * get_terminal_size().columns)

        today = fmt_datetime(t_sep=" - ")
        filename = f"users.{today}.json"
        path = f"{self.save_directory}{os.sep}{filename}"
        json_dump(data, path=path)
