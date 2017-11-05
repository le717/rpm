# -*- coding: utf-8 -*-
"""rpm - LEGO Racers mods package manager.

Created 2015-2016 Caleb Ely
<https://CodeTri.net/>

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

    @return See signature for jsonutils::read.
    """
    logging.info("Loading app settings")
    return jsonutils.read(fileName)


def save(value):
    """Write the app settings.

    @todo Do I really need this method?

    @return See signature for jsonutils::write.
    """
    jsonData = {
        "baseUrl": value
    }

    logging.info("Writing app settings to {0}".format(fileName))
    return jsonutils.write(fileName, jsonData)
