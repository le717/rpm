# -*- coding: utf-8 -*-
"""rpm - LEGO Racers mods package manager.

Created 2015-2016 Caleb Ely
<http://codetriangle.me/>

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

    @returns See signature for jsonutils::read.
    """
    logging.info("Loading app settings")
    return jsonutils.read(fileName)


def save(self, data):
    """Write the user settings.

    @param {*} data The JSON-parsable data to be written.
    @returns See signature for jsonutils::write.
    """
    logging.info("Writing user settings to {0}".format(fileName))
    return jsonutils.write(fileName, data, indent=4)
