# twitch-scraper

Twitch profile & clip scraper. Twitch API credentials are required.

## Installation

### Run without installing

```sh
uvx --from git+https://github.com/zigai/twitch-scraper.git twitch-scraper --help
```

### Install globally

```sh
uv tool install git+https://github.com/zigai/twitch-scraper.git
```

### As a dependency

```sh
uv add git+https://github.com/zigai/twitch-scraper.git
```
or
```sh
pip install git+https://github.com/zigai/twitch-scraper.git
```

## CLI usage

```
usage: twitch-scraper [--help] [-c ] [-d ] [--no-verbose]
                      SAVE-DIR CLIENT-ID BEARER {clips,profiles} ...

 _            _ _       _
| |___      _(_) |_ ___| |__    ___  ___ _ __ __ _ _ __   ___ _ __
| __\ \ /\ / / | __/ __| '_ \  / __|/ __| '__/ _` | '_ \ / _ \ '__|
| |_ \ V  V /| | || (__| | | | \__ \ (__| | | (_| | |_) |  __/ |
 \__| \_/\_/ |_|\__\___|_| |_| |___/\___|_|  \__,_| .__/ \___|_|
                                                  |_|

positional arguments:
  SAVE-DIR              directory to save files
  CLIENT-ID             twitch.tv client ID
  BEARER                twitch.tv bearer token

options:
  --help                Show this help message and exit
  -c, --cache           path to cache file
  -d, --delay           delay between requests (seconds) [default: 0.5]
  -n, --no-verbose      print status messages [default: True]

commands:
  clips                 Scrape Twitch.tv clips.
  profiles              Scrape Twitch.tv user profiles.
```

```
usage: twitch-scraper SAVE-DIR CLIENT-ID BEARER clips [--help] [-e ] [-g ]
                                                      [-l ] [-s ] [-u ]

Scrape Twitch.tv clips.

options:
  --help                Show this help message and exit
  -e, --ended-at        ending date/time
  -g, --game            Name of the game
  -l, --limit           maximum number of clips to scrape [default: 1000]
  -s, --started-at      starting date/time
  -u, --username        username of the streamer
```

```
usage: twitch-scraper SAVE-DIR CLIENT-ID BEARER profiles [--help]
                                                         USERNAMES
                                                         [USERNAMES ...]

Scrape Twitch.tv user profiles.

positional arguments:
  USERNAMES [USERNAMES ...]
                        usernames of profiles to scrape

options:
  --help                Show this help message and exit
```

## Library usage

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

## License

[MIT](LICENSE)
