# -*- coding: utf-8 -*-
"""rpm - LEGO Racers package manager.

Created 2015-2018 Caleb Ely
<https://CodeTri.net/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
import logging

from src.utils import utils, jsonutils

__all__ = ["load", "save"]

fileName = os.path.join(utils.AppUtils().config_path, "user.json")


def load():
    """Load the app settings.

    @return See signature for utils.Settings.
    """
    logging.info("Loading user settings")
    return utils.Settings(jsonutils.read(fileName))


def save(data) -> bool:
    """Write the user settings.

    @param {*} data - The JSON-parsable data to be written.
    @return {Boolean} See signature for jsonutils::write.
    """
    logging.info(f"Writing user settings to {fileName}")
    return jsonutils.write(fileName, data, indent=4)
