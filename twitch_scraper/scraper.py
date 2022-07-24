import datetime
import time
from datetime import datetime

from stdl.str_util import Color, str_with_color

from api_client import TwitchApiClient


class TwitchScraper(TwitchApiClient):

    def __init__(
        self,
        save_directory: str,
        client_id: str,
        bearer_token: str,
        verbose: bool = True,
        delay_seconds: float = 5,
    ) -> None:
        super().__init__(client_id, bearer_token, verbose)
        self.save_directory = save_directory
        self.delay_seconds = delay_seconds

    def clips(
        self,
        username: str = None,
        game: str = None,
        started_at: datetime = None,
        ended_at: datetime = None,
        limit: int = 1000,
    ):
        clips = self.get_clips(username, game, started_at, ended_at, limit)
        for i in clips:
            if self.verbose:
                print((f"{str_with_color('Downloading',Color.LIGHT_GREEN)} "
                       f"'{str_with_color(i.title,Color.BOLD)}'"
                       f" ({str_with_color(i.url,Color.LIGHT_BLUE)})"))
            i.download(directory=self.save_directory, progressbar=self.verbose)
            if self.verbose:
                print(str_with_color("_" * 64, Color.UNDERLINE))
            time.sleep(self.delay_seconds)
