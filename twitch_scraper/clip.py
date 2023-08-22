import os
import re

from stdl.dataclass import Data, dataclass
from stdl.dt import datetime, fmt_date, parse_datetime_str
from stdl.net import download
from stdl.st import StringFilter


@dataclass(order=True)
class TwitchClip(Data):
    view_count: int
    clip_id: str
    duration: float
    streamer: str
    language: str
    title: str
    created_at: datetime
    url: str
    thumbnail_url: str
    game_id: int | None = None
    creator_name: str | None = None
    embed_url: str | None = None
    video_id: int | None = None

    @property
    def file_url(self):
        """Get the clip url from thumbnail url"""
        p = r"-preview-[\d]+x[\d]+\.[\w]+"
        s = re.split(p, self.thumbnail_url)
        return s[0] + ".mp4"

    def _get_filename(self):
        dt = fmt_date(self.created_at.date())
        title = self.title.replace(".", "_").replace(" ", "_").strip()
        # game_id.streamer.view_count.duration.title.date.language.mp4
        filename = f"{self.game_id}.{self.streamer}{self.view_count}.{int(self.duration)}.{title}.{dt}.{self.language}.mp4"
        return StringFilter.filename(filename)

    def download(self, directory: str, maxsize: int | str | None = None, progressbar=False):
        path = directory + os.sep + self._get_filename()
        r = download(
            url=self.file_url, path=path, overwrite=True, progressbar=progressbar, maxsize=maxsize
        )
        return r[0]

    @staticmethod
    def from_json(data: dict):
        """TwitchClip from json object returned by Twitch Helix API"""
        return TwitchClip(
            clip_id=data["id"],
            url=data["url"],
            embed_url=data["embed_url"],
            streamer=data["broadcaster_name"],
            creator_name=data["creator_name"],
            video_id=data["video_id"],
            game_id=data["game_id"],
            language=data["language"],
            title=data["title"],
            view_count=data["view_count"],
            created_at=parse_datetime_str(data["created_at"]),
            thumbnail_url=data["thumbnail_url"],
            duration=data["duration"],
        )
