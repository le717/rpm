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

from src.utils import utils


class UserSettings:

    def __init__(self):
        self.__file = os.path.join(utils.AppUtils().configPath, "user.json")

    def load(self):
        """Load the app settings.

        @returns {Boolean} True if app settings were loaded, False otherwise.
        """
        try:
            # Make sure it exists
            if os.path.exists(self.__file):
                logging.info("Reading user settings from {0}".format(
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
            logging.warning("The stored user settings are not available!")
            return None

    def save(self, appOpts):
        """Write the user settings.

        @returns {Boolean} True if user settings were written, False otherwise.
        """
        try:
            logging.info("Writing user settings to {0}".format(self.__file))
            with open(self.__file, "wt", encoding="utf-8") as f:
                f.write(json.dumps(appOpts, indent=4, sort_keys=True))
            return True

        # Silently fail
        except PermissionError:
            logging.warning("Settings could not be saved!")
            return False
