# -*- coding: utf-8 -*

import src.constants as const
import src.init.help as init
import src.install.help as install
import src.settings.help as settings


def main(command=None):
    commandsAvailable = {
        "init": init.main,
        "install": install.main,
        "settings": settings.main
    }

    # General help is requested
    if command is None:
        message = f"""Usage: {const.APP_NAME} <command>

where command is one of:
    help, init, install, settings

{const.APP_NAME} help <command> search for help on <command>"""
        print(message)

    # Specific command help
    elif command in commandsAvailable.keys():
        commandsAvailable[command]()
