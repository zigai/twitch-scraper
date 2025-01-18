# Twitch scraper
Twitch clip/profile scraper.
Twitch API credentials are required.

# Installation
```
pip install git+https://github.com/zigai/twitch-scraper.git
```
# CLI usage
```
usage: twitch-scraper [-h] [-d] [-c] [--verbose | --no-verbose] SAVE-DIR CLIENT-ID BEARER {clips,profiles} ...

 _            _ _       _
| |___      _(_) |_ ___| |__    ___  ___ _ __ __ _ _ __   ___ _ __
| __\ \ /\ / / | __/ __| '_ \  / __|/ __| '__/ _` | '_ \ / _ \ '__|
| |_ \ V  V /| | || (__| | | | \__ \ (__| | | (_| | |_) |  __/ |
 \__| \_/\_/ |_|\__\___|_| |_| |___/\___|_|  \__,_| .__/ \___|_|
                                                  |_|

positional arguments:
  SAVE-DIR                              directory to save files [type: str] (*)
  CLIENT-ID                             twitch.tv client ID [type: str] (*)
  BEARER                                twitch.tv bearer token [type: str] (*)
  {clips,profiles} ...

options:
  -h, --help                            show this help message and exit
  -d, --delay                           delay between requests (seconds) [type: float, default=0.5]
  -c, --cache                           path to cache file [type: str?]
  --verbose, --no-verbose               print status messages.

commands:
   clips            Scrape Twitch.tv clips.
   profiles         Scrape Twitch.tv user profiles
```

```
usage: twitch-scraper SAVE-DIR CLIENT-ID BEARER clips [-h] [-u] [-g] [-s] [-e] [-l]

Scrape Twitch.tv clips.

options:
  -h, --help            show this help message and exit
  -u, --username    username of the streamer [type: str?]
  -g, --game        Name of the game [type: str?]
  -s, --started-at  starting date/time [type: datetime?]
  -e, --ended-at    ending date/time [type: datetime?]
  -l, --limit       maximum number of clips to scrape [type: int, default=1000]
```

```
usage: twitch-scraper SAVE-DIR CLIENT-ID BEARER profiles [-h] [USERNAMES ...]

Scrape Twitch.tv user profiles

positional arguments:
  USERNAMES   usernames of profiles to scrape [type: list[str]] (*)

options:
  -h, --help  show this help message and exit
```

# Library usage
```python
from datetime import datetime, timedelta
from twitch_scraper import TwitchScraper

scraper = TwitchScraper(
    save_dir="./clips",
    client_id=...,
    bearer=...,
)

today = datetime.today()
scraper.clips(
    game="League of Legends",
    started_at=today - timedelta(days=7),
    ended_at=today,
    limit=50,
)
```


# License
[MIT License](https://github.com/zigai/twitch-scraper/blob/master/LICENSE)
