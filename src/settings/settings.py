# -*- coding: utf-8 -*-
"""pire - LEGO Racers mods package manager.

Created 2015 Caleb Ely
<http://codetriangle.me/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
import logging

from . import user as userSettings


def __getVersion(gamePath):
    """Detect game release year.

    @param {String} gamePath An absolute path to the game installation.
    @returns {String|NoneType} The release year or None if unavailable.
    """
    version = None
    # Open the exe and read a small part of it
    try:
        with open(os.path.join(gamePath, "LEGORacers.exe"), "rb") as f:
            offset = f.readlines()[1][8:20]

        # This is a 1999 release
        if offset in (b"\xb7S\xfeK\xf32\x90\x18\xf32\x90\x18" or
                      b"bPE\x00\x00L\x01\x08\x00\xf1\xdb)7"):
            logging.info("According to the offset, this is a 1999 release")
            version = "1999"

        # This is a 2001 release
        elif offset == b"\xd7\xf2J\x1a\x93\x93$I\x93\x93$I":
            logging.info("According to the offset, this is a 2001 release")
            version = "2001"
        return version

    # We could not find the data we wanted
    except IndexError:
        logging.warning("Game release version could not be determined!")
        return version


def __confirmGame(gamePath):
    """Confirm a game installation at the given path.

    @param {String} gamePath An absolute path to the game installation.
    @returns {Boolean} True if a game installation was confirmed,
                       False otherwise.
    """
    gamePath = os.path.abspath(gamePath)

    # The path does not exist
    if not os.path.isdir(gamePath):
        logging.warning("Could not find game installation at {0}".format(
                        gamePath))
        return False

    # Look for the expected game files
    exePath = os.path.join(gamePath, "LEGORacers.exe")
    jamPath = os.path.join(gamePath, "LEGO.JAM")
    dllPath = os.path.join(gamePath, "GolDP.dll")

    # The necessary files were found
    if (
        os.path.isfile(exePath) and
        os.path.isfile(jamPath) and
        os.path.isfile(dllPath)
    ):
        logging.info("Game installation found at {0}".format(gamePath))
        return True

    logging.warning("Could not find game installation at {0}".format(
                    gamePath))
    return False


def main(*args):
    pathExists = False
    appOpts = {
        "gameLocation": None,
        "gameRelease": None
    }

    # Keep asking for a path until we get one
    while not pathExists:
        gamePath = input("Please enter the path to your game installation:\n")
        pathExists = __confirmGame(gamePath)

    # Extract the information we need
    appOpts["gameLocation"] = os.path.abspath(gamePath.replace("\\", "/"))
    appOpts["gameRelease"] = __getVersion(gamePath)

    # Save the settings
    userSettings.save(appOpts)
    print("Settings were successfully saved")
    logging.info("User settings successfully saved")
    return True
