# -*- coding: utf-8 -*
"""pire - LEGO Racers mods package manager.

Created 2015-2016 Caleb Ely
<http://codetriangle.me/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import sys

from src.help import help
from src.init import init
from src.install import install
from src.settings import settings
from src.utils import logger


def getArguments():
    """Get the app arguments.

    @returns {Dicionary.<command:string, value:string>}.
    """
    argu = sys.argv
    result = {
        "command": None,
        "value": None
    }

    # Collect the arguments passed
    try:
        result["command"] = argu[1]
        result["value"] = argu[2]
    except IndexError:
        return result

    return result


def main():
    """Run the application."""
    # Start app logging
    print()
    logger.main()

    # Define all available commands
    commandsAvailable = {
        "help": help.main,
        "init": init.main,
        "install": install.main,
        "settings": settings.main
    }

    # Get the passed arguments
    arguments = getArguments()

    # Run the function appropriate for the given command
    if arguments["command"] in commandsAvailable.keys():
        commandsAvailable[arguments["command"]](arguments["value"])

    # Only the app was run, display help
    elif arguments["command"] is None:
        commandsAvailable["help"]()

    raise SystemExit(0)
