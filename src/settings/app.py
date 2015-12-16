# -*- coding: utf-8 -*-


import os
import json
import logging

from src.utils import utils
from src import constants as const


class AppSettings:

    def __init__(self):
        self.__file = os.path.join(utils.AppUtils().configPath,
                                   "{0}.json".format(const.APP_NAME))

    def load(self):
        """Load the app settings.

        @returns {Boolean} True if app settings were loaded, False otherwise.
        """
        try:
            # Make sure it exists
            if os.path.exists(self.__file):
                logging.info("Reading app settings from {0}".format(
                             self.__file))
                with open(self.__file, "rt", encoding="utf-8") as f:
                    data = json.load(f)
                return data

            # The settings have not been previously written
            else:
                logging.warning("The stored settings are not available!")
                return None

        # The file is not valid JSON, sliently fail
        except ValueError:
            logging.warning("The stored settings are not available!")
            return None

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
