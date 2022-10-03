import argparse
from secrets import *

from twitch_scraper.scraper import TwitchScraper

parser = argparse.ArgumentParser(add_help=True)
parser.description = "Twitch Scraper"
parser.add_argument("--client_id", type=str, required=True, help="")
parser.add_argument("--bearer_token", type=str, required=True, help="")
parser.add_argument("--save_directory", type=str, required=True, help="")
sub_parser = parser.add_subparsers(dest="subparser")
# -----------------------------------------------------
clips_parser = sub_parser.add_parser("clips")
clips_parser.description = "Scrape Twitch.tv clips"
clips_parser.add_argument(
    "--username",
    required=False,
    default=None,
    type=str,
    help="username of the broadcaster for whom clips are returned",
)
clips_parser.add_argument(
    "--game",
    required=False,
    default=None,
    type=str,
    help="name of the game for which clips are returned",
)
clips_parser.add_argument(
    "--started_at",
    required=False,
    default=None,
    type=str,
    help="starting date/time for returned clips",
)
clips_parser.add_argument(
    "--ended_at",
    required=False,
    default=None,
    type=str,
    help="ending date/time for returned clips",
)
clips_parser.add_argument(
    "--limit",
    required=False,
    default=1000,
    type=int,
    help="how many clips to return ",
)
# -----------------------------------------------------
profiles_parser = sub_parser.add_parser("profiles")
profiles_parser.description = "Scrape Twitch.tv profiles"
profiles_parser.add_argument(
    "--usernames",
    type=list,
    required=True,
    help="List of username to scrape. Seperated by ','",
)
args = parser.parse_args()
print(args)
# How to split arguments between class init method and command?
# Option #1: in add_argument call add a 'dest' parameter with a string like {owner}.{flag_name}
