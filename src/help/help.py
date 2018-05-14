# -*- coding: utf-8 -*

import src.constants as const
import src.init.help as init
import src.install.help as install
import src.settings.help as settings


def main(command: str):
    commands_available = {
        "init": init.main,
        "install": install.main,
        "settings": settings.main
    }
    commands_available_keys = commands_available.keys()

    # Specific command help
    if command in commands_available_keys:
        commands_available[command]()

    # General help is requested
    else:
        message = f"""{const.APP_NAME} {const.VERSION}

USAGE
{const.APP_NAME} <command>

where command is one of:
    {", ".join(commands_available_keys)}

DESCRIPTION
Run an available command in {const.APP_NAME}. To display the help text for a
specific command, run {const.APP_NAME} help <command>.
Run {const.APP_NAME} help to display this message again at any time.
"""
        print(message)
