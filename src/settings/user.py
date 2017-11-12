# -*- coding: utf-8 -*-
"""rpm - LEGO Racers mods package manager.

Created 2015-2017 Caleb Ely
<https://CodeTri.net/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
import logging

from src.utils import utils, jsonutils

__all__ = ("load", "save")

fileName = os.path.join(utils.AppUtils().configPath, "user.json")


def load():
    """Load the app settings.

    @return See signature for jsonutils::read.
    """
    logging.info("Loading user settings")
    return utils.Settings(jsonutils.read(fileName))


def save(data):
    """Write the user settings.

    @param {*} data The JSON-parsable data to be written.
    @return See signature for jsonutils::write.
    """
    logging.info("Writing user settings to {0}".format(fileName))
    return jsonutils.write(fileName, data, indent=4)
