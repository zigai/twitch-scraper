from stdl.dt import datetime, datetime_fmt, time
from stdl.fs import json_dump, os
from stdl.log import br
from stdl.st import FG, colored

from twitch_scraper.client import TwitchApiClient


class TwitchScraper(TwitchApiClient):
    """
    Twitch.tv scraper

    Args:
        save_dir (str): save directory
        client_id (str): twitch.tv client ID
        bearer (str): twitch.tv bearer token
        verbose (bool): print status messages
        delay (float): delay between requests (seconds)
        cache (str): path to cache file. cache is used to avoid duplicate requests
    """

    def __init__(
        self,
        save_dir: str,
        client_id: str,
        bearer: str,
        delay: float = 0.5,
        cache: str | None = None,
        verbose: bool = True,
    ) -> None:
        """
        Twitch.tv clip / profile scraper

        Args:
            save_dir (str): directory to save files
            client_id (str): twitch.tv client ID
            bearer (str): twitch.tv bearer token
            delay (float): delay between requests (seconds)
            cache (str): path to cache file
            verbose (bool): print status messages
        """
        super().__init__(client_id, bearer, cache, verbose)
        self.save_directory = save_dir
        self.delay_seconds = delay

    def _log(self, text: str):
        if self.verbose:
            print(text)

    def _br(self):
        if self.verbose:
            br()

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
            game (str): Name of the game
            started_at (datetime.datetime): starting date/time
            ended_at (datetime.datetime): ending date/time
            limit (int): maximum number of clips to scrape

        """
        clips = self.get_clips(username, game, started_at, ended_at, limit)
        for clip in clips:
            self._log(
                (
                    f"{colored('Downloading',FG.LIGHT_GREEN)} "
                    f"'{colored(clip.title,FG.BOLD)}'"
                    f" ({colored(clip.url,FG.LIGHT_BLUE)})"
                )
            )
            clip.download(directory=self.save_directory, progressbar=self.verbose)
            self._br()
            time.sleep(self.delay_seconds)

    def profiles(self, usernames: list[str]):
        """
        Scrape Twitch.tv user profiles

        Args:
            usernames (list[str]) : usernames of profiles to scrape

        """
        data = []
        for username in usernames:
            user = self.get_user(username=username)
            self._log(f"Getting data for user '{colored(username, FG.LIGHT_BLUE)}' ...")
            if user is None:
                self._log(colored(f"User '{username}' not found", FG.RED))
            else:
                data.append(user.dict())
                time.sleep(self.delay_seconds)
                self._br()

        today = datetime_fmt(tsep=" - ")
        filename = f"users.{today}.json"
        path = f"{self.save_directory}{os.sep}{filename}"
        json_dump(data, path=path)
