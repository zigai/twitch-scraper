# Twitch scraper
Twitch clip/profile scraper.
Twitch API credentials are required.

# Installation
```
pip install git+https://github.com/zigai/twitch-scraper.git
```
# CLI usage
```
usage: twitch-scraper [-h] {clips,profiles} ...
 _            _ _       _
| |___      _(_) |_ ___| |__    ___  ___ _ __ __ _ _ __   ___ _ __
| __\ \ /\ / / | __/ __| '_ \  / __|/ __| '__/ _` | '_ \ / _ \ '__|
| |_ \ V  V /| | || (__| | | | \__ \ (__| | | (_| | |_) |  __/ |
 \__| \_/\_/ |_|\__\___|_| |_| |___/\___|_|  \__,_| .__/ \___|_|
                                                  |_|

positional arguments:
  {clips,profiles}

options:
  -h, --help        show this help message and exit

commands:
  clips             Scrape Twitch.tv clips
  profiles          Scrape Twitch.tv user profile
```

```
usage: twitch-scraper clips [-h] -s -c -b [-v] [-d] [-ca] [-u] [-g] [-st] [-e] [-l]

Scrape Twitch.tv clips

options:
  -h, --help        show this help message and exit
  -s, --save-dir    directory to save files | str (*)
  -c, --client-id   twitch.tv client ID | str (*)
  -b, --bearer      twitch.tv bearer token | str (*)
  -v, --verbose     print status messages | bool = True
  -d, --delay       delay between requests (seconds) | float = 0.5
  -ca, --cache      path to cache file. cache is used to avoid duplicate requests | str
  -u, --username    username of the streamer | str
  -g, --game        name of the game | str
  -st, --started-at
                        Starting date/time | datetime
  -e, --ended-at    Ending date/time | datetime
  -l, --limit       Number of clips to scrape | int = 1000
```

```
usage: twitch-scraper profiles [-h] -s -c -b [-v] [-d] [-ca] -u

Scrape Twitch.tv user profiles

options:
  -h, --help       show this help message and exit
  -s, --save-dir   directory to save files | str (*)
  -c, --client-id  twitch.tv client ID | str (*)
  -b, --bearer     twitch.tv bearer token | str (*)
  -v, --verbose    print status messages | bool = True
  -d, --delay      delay between requests (seconds) | float = 0.5
  -ca, --cache     path to cache file | str
  -u, --usernames  usernames of profiles to scrape | list[str] (*)
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
