import datetime
from dataclasses import asdict, dataclass


@dataclass()
class TwitchUser:
    user_id: str
    username: str
    display_name: str
    broadcaster_type: str
    created_at: datetime.datetime
    view_count: int
    description: str
    email: str | None = None
    offline_image_url: str | None = None
    profile_image_url: str | None = None

    @property
    def profile_url(self):
        return "https://www.twitch.tv/" + self.username

    def dict(self):
        return asdict(self)
