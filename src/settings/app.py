# -*- coding: utf-8 -*-
"""pire - LEGO Racers mods package manager.

Created 2015 Caleb Ely
<http://codetriangle.me/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
import json
import logging

from src import constants as const
from src.utils import utils, jsonutils


class AppSettings:

    def __init__(self):
        self.__file = os.path.join(utils.AppUtils().configPath,
                                   "{0}.json".format(const.APP_NAME))

    def load(self):
        """Load the app settings.

        @returns {@todo|Boolean} @todo,
                                 False if app settings were not loaded.
        """
        return jsonutils.read(self.__file)

    def save(self, value):
        """Write the app settings.

        @todo Do I really need this method?

        @returns {Boolean} True if app settings were written, False otherwise.
        """
        try:
            jsonData = {
                "baseUrl": value
            }

            logging.info("Writing app settings to {0}".format(self.__file))
            with open(self.__file, "wt", encoding="utf-8") as f:
                f.write(json.dumps(jsonData, sort_keys=True))
            return True

        # Silently fail
        except PermissionError:
            logging.warning("Settings could not be saved!")
            return False
