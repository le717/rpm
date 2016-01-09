# -*- coding: utf-8 -*-
"""pire - LEGO Racers mods package manager.

Created 2015 Caleb Ely
<http://codetriangle.me/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
import logging

from src.utils import utils, jsonutils

__all__ = ("load", "save")

fileName = os.path.join(utils.AppUtils().configPath, "app.json")


def load():
    """Load the app settings.

    @returns See signature for jsonutils::read.
    """
    logging.info("Loading app settings")
    return jsonutils.read(fileName)


def save(value):
    """Write the app settings.

    @todo Do I really need this method?

    @returns See signature for jsonutils::write.
    """
    jsonData = {
        "baseUrl": value
    }

    logging.info("Writing app settings to {0}".format(fileName))
    return jsonutils.write(fileName, jsonData)
