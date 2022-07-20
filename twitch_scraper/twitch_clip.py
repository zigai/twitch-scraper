import datetime
import os
import re
from dataclasses import dataclass

from dathas import Dathas
from stdl.datetime_util import Date
from stdl.net_util import download_file
from stdl.str_util import FilterStr


@dataclass(order=True)
class TwitchClip(Dathas):
    views: int
    clip_id: str
    duration: float
    streamer: str
    language: str
    game: str
    title: str
    created_at: datetime.datetime
    url: str
    thumbnail_url: str
    creator_name: str = None
    embed_url: str = None

    @property
    def file_url(self):
        """Get the clip url from thumbnail url"""
        p = r"-preview-[\d]+x[\d]+\.[\w]+"
        s = re.split(p, self.thumbnail_url)
        return s[0] + ".mp4"

    def get_filename(self):
        dt = Date.format(self.created_at.date())
        title = FilterStr.file_name(self.title).replace(".", "_").replace(" ", "_").strip()
        filename = f"{self.game}.{self.streamer}{self.views}.{int(self.duration)}.{title}.{dt}{self.language}.mp4"
        return filename

    def download(self, directory: str, progressbar=False):
        path = directory + os.sep + self.get_filename()
        path = FilterStr.file_name(path)
        download_file(url=self.file_url, path=path, overwrite=True, progressbar=progressbar)
