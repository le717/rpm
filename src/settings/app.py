# -*- coding: utf-8 -*-
"""pire - LEGO Racers mods package manager.

Created 2015 Caleb Ely
<http://codetriangle.me/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
import logging

from src import constants as const
from src.utils import utils, jsonutils


class AppSettings:

    def __init__(self):
        self.__file = os.path.join(utils.AppUtils().configPath,
                                   "{0}.json".format(const.APP_NAME))

    def load(self):
        """Load the app settings.

        @returns See documentation for jsonutils::read.
        """
        logging.info("Loading app settings")
        return jsonutils.read(self.__file)

    def save(self, value):
        """Write the app settings.

        @todo Do I really need this method?

        @returns See documentation for jsonutils::write.
        """
        jsonData = {
            "baseUrl": value
        }

        logging.info("Writing app settings to {0}".format(self.__file))
        return jsonutils.write(self.__file, jsonData)
