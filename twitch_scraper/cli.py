def main():
    from interfacy_cli import CLI
    from stdl.str_u import FG, ST, colored

    from twitch_scraper.scraper import TwitchScraper

    description = """
    ______           _   __         __         ____                                   
    /_  __/ _    __  (_) / /_ ____  / /        / __/ ____  ____ ___ _  ___  ___   ____
    / /   | |/|/ / / / / __// __/ / _ \      _\ \  / __/ / __// _ `/ / _ \/ -_) / __/
    /_/    |__,__/ /_/  \__/ \__/ /_//_/     /___/  \__/ /_/   \_,_/ / .__/\__/ /_/   
                                                                    /_/               
    """

    description = colored(description, FG.MAGENTA, style=ST.BOLD)

    CLI(TwitchScraper, description=description)


if __name__ == "__main__":
    main()
