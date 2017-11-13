# -*- coding: utf-8 -*-
"""rpm - LEGO Racers mods package manager.

Created 2015-2017 Caleb Ely
<https://CodeTri.net/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
import platform

from src import constants as const

__all__ = ("AppUtils", "Settings")


class Settings:

    """Generic settings class.

    This is used as a thin wrapper around user and app settings
    to more gracefully handle errors.
    """

    def __init__(self, settings):
        """Initialize class properties.

        @param {Dictionary} The settings dictionary to use.
        """
        self.__settings = settings

    def get(self, key):
        """Get a specific setting's value.

        @param {String} key The value for the given setting key.
        @return {*|NoneType}
        """
        if self.__settings is None:
            return None
        return self.__settings.get(key)

    def get_all(self):
        """Get the entire settings dictionary.

        @return {Dictionary}
        """
        return self.__settings


class AppUtils:

    """Utility properties and methods.

    Exposes the following public properties and methods:
    * isWindows {Boolean} True if the user is running a Windows OS.
    * configPath {String} An absolute path to the app's configuration folder.
    * cachePath {String} An absolute path to the download cache folder.
    * tempPath {String} An absolute path to a temporary files folder.
    """

    def __init__(self):
        """Initalize public properties and run utility functions."""
        self.isWindows = "Windows" in platform.platform()
        self.configPath = self.__getConfigPath()
        self.cachePath = self.__createFolder(
            os.path.join(self.configPath, "cache"))
        self.tempPath = self.__createFolder(
            os.path.join(self.configPath, "temp"))

    def __getConfigPath(self):
        """Get the file path where configuration files will be stored.

        On Windows, the root folder is %AppData%, while on macOS and Linux
        it is ~. On all platforms, the rest of the path is
        Triangle717/APP_NAME.

        @return {String} The configuration path.
        """
        root = os.path.expanduser("~")
        if self.isWindows:
            root = os.path.expandvars("%AppData%")

        # Create the path if needed
        path = os.path.join(root, "Triangle717", const.APP_NAME)
        if not os.path.exists(path):
            os.makedirs(path)

        return path

    def __createFolder(self, path):
        """Create the given folder and all preceeding folders.

        @param {String} path An absolute path for the desired folder.
        @return {String} The folder path given in the path parameter.
        """
        if not os.path.exists(path):
            os.makedirs(path)
        return path
