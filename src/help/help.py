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
        message = """Usage: {0} <command>

where command is one of:
    help, init, install, settings

{0} help <command>    search for help on <command>""".format(const.APP_NAME)
        print(message)

    # Specific command help
    elif command in commandsAvailable.keys():
        commandsAvailable[command]()
