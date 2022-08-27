import datetime

from stdl.dataclass import Data, dataclass


@dataclass()
class TwitchUser(Data):
    user_id: str
    username: str
    display_name: str
    broadcaster_type: str
    created_at: datetime.datetime
    view_count: int
    description: str
    email: str = None
    offline_image_url: str = None
    profile_image_url: str = None

    @property
    def twitch_url(self):
        return "https://www.twitch.tv/" + self.username
