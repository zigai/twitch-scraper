def cli():
    from interfacy_cli import CLI
    from stdl.str_u import FG, ST, colored

    from twitch_scraper.scraper import TwitchScraper

    description = """
 _            _ _       _                                          
| |___      _(_) |_ ___| |__    ___  ___ _ __ __ _ _ __   ___ _ __ 
| __\ \ /\ / / | __/ __| '_ \  / __|/ __| '__/ _` | '_ \ / _ \ '__|
| |_ \ V  V /| | || (__| | | | \__ \ (__| | | (_| | |_) |  __/ |   
 \__| \_/\_/ |_|\__\___|_| |_| |___/\___|_|  \__,_| .__/ \___|_|   
                                                  |_|              
    """

    description = colored(description, FG.MAGENTA, style=ST.BOLD)

    CLI(TwitchScraper, description=description)


if __name__ == "__main__":
    cli()
