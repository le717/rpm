# -*- coding: utf-8 -*-
"""pire - LEGO Racers mods package manager.

Created 2015 Caleb Ely
<http://codetriangle.me/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
import sys
import logging
import platform
from datetime import datetime

from src import constants as const
from . import utils


def main():
    """Application logging."""
    Utils = utils.AppUtils()
    configPath = Utils.configPath
    loggingFile = os.path.join(configPath, "{0}.log".format(const.APP_NAME))

    # Get the Python architecture
    pythonArch = "x64"
    if sys.maxsize < 2 ** 32:
        pythonArch = "x86"

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s : %(levelname)s : %(message)s",
        filename=loggingFile,
        filemode="a"
    )

    logging.debug("Begin logging to {0}".format(loggingFile))
    logging.debug("Timestamp: {0}".format(datetime.utcnow().isoformat()))
    logging.debug("You are running {0} {1} {2} on {3} {4}.".format(
        platform.python_implementation(),
        pythonArch,
        platform.python_version(),
        platform.machine(),
        platform.platform())
    )
