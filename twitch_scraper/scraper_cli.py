from secrets import *

from twitch_scraper import TwitchScraper


def main():
    scraper = TwitchScraper(
        client_id=client_id,
        bearer_token=bearer,
        save_directory="/mnt/e/data/scraping/twitch/clips",
    )
    scraper.clips(username="jankos", limit=10)


if __name__ == '__main__':
    main()
