from dataclasses import replace

from interfacy import Interfacy, Param
from interfacy.help.content import HelpContent
from interfacy.plugins import HelpHookContext, InterfacyPlugin
from stdl.st import FG, ST, colored
from typing_extensions import override

from twitch_scraper.scraper import TwitchScraper

PROGRAM_NAME = "twitch-scraper"

DESCRIPTION = colored(
    r""" _            _ _       _
| |___      _(_) |_ ___| |__    ___  ___ _ __ __ _ _ __   ___ _ __
| __\ \ /\ / / | __/ __| '_ \  / __|/ __| '__/ _` | '_ \ / _ \ '__|
| |_ \ V  V /| | || (__| | | | \__ \ (__| | | (_| | |_) |  __/ |
 \__| \_/\_/ |_|\__\___|_| |_| |___/\___|_|  \__,_| .__/ \___|_|
                                                  |_|""",
    FG.MAGENTA,
    style=ST.BOLD,
)


class HelpHeader(InterfacyPlugin):
    @override
    def transform_help(self, context: HelpHookContext, content: HelpContent) -> HelpContent:
        sections = []
        for section in content.sections:
            if section.kind == "usage":
                prefix, separator, arguments = section.text.partition(" ")
                _, separator, arguments = arguments.partition(" ")
                section = replace(section, text=f"{prefix} {PROGRAM_NAME}{separator}{arguments}")
            elif section.kind == "description":
                section = replace(section, text=DESCRIPTION)
            sections.append(section)

        return replace(content, sections=tuple(sections))


def cli() -> None:
    app = Interfacy(plugins=[HelpHeader()])
    app.add_command(
        TwitchScraper,
        params={"verbose": Param(negative_flags=("-n", "--no-verbose"))},
    )
    app.run()


if __name__ == "__main__":
    cli()
