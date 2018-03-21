# -*- coding: utf-8 -*
"""rpm - LEGO Racers mods package manager.

Created 2015-2018 Caleb Ely
<https://CodeTri.net/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import sys

from src.help import help
from src.init import init
from src.install import install
from src.settings import settings
from src.utils import logger


def get_arguments():
    """Get the app arguments.

    @return {Dicionary.<command:string, value:string>}.
    """
    result = {
        "command": None,
        "value": None
    }

    # Collect the arguments passed
    try:
        result["command"] = sys.argv[1]
        result["value"] = sys.argv[2]
    except IndexError:
        pass
    return result


def main():
    """Run the application."""
    logger.main()

    # Define all available commands
    commmands = {
        "help": help.main,
        "init": init.main,
        "install": install.main,
        "settings": settings.main
    }

    # Get the passed arguments
    arguments = get_arguments()

    # Run the function appropriate for the given command
    if arguments["command"] in commmands.keys():
        commmands[arguments["command"]](arguments["value"])

    # Only the app was run, display help
    elif arguments["command"] is None:
        commmands["help"]()

    raise SystemExit(0)
