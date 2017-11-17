# -*- coding: utf-8 -*-
"""rpm - LEGO Racers mods package manager.

Created 2015-2017 Caleb Ely
<https://CodeTri.net/>

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
    config_path = utils.AppUtils().configPath
    log_file = os.path.join(config_path, "{0}.log".format(const.APP_NAME))

    # Get the Python architecture
    py_arch = "x64"
    if sys.maxsize < 2 ** 32:
        py_arch = "x86"

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s : %(levelname)s : %(message)s",
        filename=log_file,
        filemode="a"
    )

    logging.debug("Begin logging to {0}".format(log_file))
    logging.debug("Timestamp: {0}".format(datetime.utcnow().isoformat()))
    logging.debug("You are running {0} {1} {2} on {3} {4}.".format(
        platform.python_implementation(),
        py_arch,
        platform.python_version(),
        platform.machine(),
        platform.platform())
    )
