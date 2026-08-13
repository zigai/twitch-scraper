import datetime
from dataclasses import dataclass

from twitch_scraper.util import JsonValue


@dataclass
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
    def profile_url(self) -> str:
        return "https://www.twitch.tv/" + self.username

    def dict(self) -> dict[str, JsonValue]:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "display_name": self.display_name,
            "broadcaster_type": self.broadcaster_type,
            "created_at": self.created_at.isoformat(),
            "view_count": self.view_count,
            "description": self.description,
            "email": self.email,
            "offline_image_url": self.offline_image_url,
            "profile_image_url": self.profile_image_url,
        }
