# -*- coding: utf-8 -*-
"""pire - LEGO Racers mods package manager.

Created 2015 Caleb Ely
<http://codetriangle.me/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
import platform

from src import constants as const

__all__ = ("AppUtils")


class AppUtils:

    """Utility properties and methods.

    Exposes the following public properties and methods:
    * isWindows {Boolean} True if the user is running a Windows OS.
    * configPath {String} An absolute path to the app's configuration folder.
    * cachePath {String} An absolute path to the download cache folder.
    """

    def __init__(self):
        """Initalize public properties and run utility functions."""
        self.isWindows = "Windows" in platform.platform()
        self.configPath = self.__getConfigPath()
        self.cachePath = os.path.join(self.configPath, "cache")

    def __getConfigPath(self):
        """Get the file path where configuration files will be stored.

        On Windows, the root folder is %AppData%, while on Mac OS X and Linux
        it is ~. On all platforms, the rest of the path is
        Triangle717/APP_NAME.

        @returns {String} The configuration path.
        """
        root = os.path.expanduser("~")
        if self.isWindows:
            root = os.path.expandvars("%AppData%")

        # Create the path if needed
        path = os.path.join(root, "Triangle717", const.APP_NAME)
        if not os.path.exists(path):
            os.makedirs(path)

        # Create the cache path
        cachePath = os.path.join(path, "cache")
        if not os.path.exists(cachePath):
            os.makedirs(cachePath)
        return path
