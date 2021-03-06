# -*- coding: utf-8 -*-
"""rpm - LEGO Racers package manager.

Created 2015-2018 Caleb Ely
<https://CodeTri.net/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
import platform
from clint.textui import colored

from src import constants as const

__all__ = ["AppUtils", "Settings", "display_message"]


class Settings:

    """Generic settings class.

    This is used as a thin wrapper around user settings
    to more gracefully handle errors.
    """

    def __init__(self, settings: dict):
        """Initialize class properties.

        @param {Dictionary} The settings dictionary to use.
        """
        self.__settings = settings

    def get(self, key: str):
        """Get a specific setting's value.

        @param {String} key The value for the given setting key.
        @return {*|NoneType}
        """
        if self.__settings is None:
            return None
        return self.__settings.get(key)

    def get_all(self) -> dict:
        """Get the entire settings dictionary.

        @return {Dictionary}
        """
        return self.__settings


class AppUtils:

    """Utility properties and methods.

    Exposes the following public properties and methods:
    * is_windows {Boolean} True if the user is running a Windows OS.
    * config_path {String} An absolute path to the app's configuration folder.
    * temp_path {String} An absolute path to a temporary files folder.
    """

    def __init__(self):
        """Initalize public properties and run utility functions."""
        self.is_windows = "Windows" in platform.platform()
        self.config_path = self.__get_config_path()
        self.temp_path = self.__create_folder(
            os.path.join(self.config_path, "temp"))

    def __get_config_path(self) -> str:
        """Get the file path where configuration files will be stored.

        On Windows, the root folder is %AppData%, while on macOS and Linux
        it is ~./config. On all platforms, the rest of the path is APP_NAME.

        @return {String} The configuration path.
        """
        root = os.path.expanduser(os.path.join("~", ".config"))
        if self.is_windows:
            root = os.path.expandvars("%AppData%")

        # Create the path if needed
        path = os.path.join(root, const.APP_NAME)
        if not os.path.exists(path):
            os.makedirs(path)

        return path

    def __create_folder(self, path: str) -> str:
        """Create the given folder and all preceeding folders.

        @param {String} path An absolute path for the desired folder.
        @return {String} The folder path given in the path parameter.
        """
        if not os.path.exists(path):
            os.makedirs(path)
        return path


def display_message(error: dict) -> bool:
    # Determine the proper color to use
    # Red for errors, yellow for warnings
    color = (colored.red if error["result"] == "error"
             else colored.yellow)
    print(color(
        f"{error['result'].capitalize()}: {error['message']}",
        bold=True
    ))

    # If this is an error, we'll need to abort the process
    # once all errors are reported
    if error["result"] == "error":
        return True
    return False
