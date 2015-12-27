# -*- coding: utf-8 -*-
"""pire - LEGO Racers mods package manager.

Created 2015 Caleb Ely
<http://codetriangle.me/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
import shutil
import logging

from src.settings import user
from src.lib import JAMExtractor


def __extractJAM(path):
    """Helper function to extract the JAM archive.

    @param {String} path Absolute path to game installation.
    @returns {Boolean} True if extraction was successful, False otherwise.
    """
    return JAMExtractor.extract(os.path.join(path, "LEGO.JAM"), False)


def __buildJAM(path):
    """Helper function to build the JAM archive.

    @param {String} path Absolute path to game installation.
    @returns {Boolean} True if build was successful, False otherwise.
    """
    return JAMExtractor.build(os.path.join(path, "LEGO"), False)


def __findExtractedJam(path):
   """Find a possible pre-extracted JAM archive.

    @param {String} path Absolute path to game installation.
    @returns {Tuple} @todo
    """
    results = (False,)
    extractedPaths = (
        (os.path.join(path, "MENUDATA"),
         os.path.join(path, "GAMEDATA")),
        (os.path.join(path, "LEGO", "MENUDATA"),
         os.path.join(path, "LEGO", "GAMEDATA"))
    )

    # The MENUDATA/GAMEDATA folders already exist
    for pathGroup in extractedPaths:
        if os.path.isdir(pathGroup[0]) and os.path.isdir(pathGroup[1]):
            # Get the exact path detected
            extractedPath = None
            if extractedPaths.index(pathGroup) == 0:
                extractedPath = path
            else:
                extractedPath = os.path.join(path, "LEGO")

            results = (True, extractedPath)
            break

    return results


def main(action):
    # Get the user settings
    settings = user.UserSettings().load()

    # We do not have any settings
    if settings is None:
        logging.warning("User has not yet configured settings")
        print("You need to configure your settings before installing!")
        return False

    # This game release requires a JAM archive
    needsJam = (True if settings["gameRelease"] in (None, "1999") else False)

    # Find possible pre-extracted files
    preExtracted = __findExtractedJam(settings["gameLocation"])

    # Perform the desired action
    if action == "extract" and needsJam:
        logging.info("Extracting LEGO.JAM")
        return __extractJAM(settings["gameLocation"])

    elif action == "build" and needsJam:
        logging.info("Building LEGO.JAM")
        r = __buildJAM(settings["gameLocation"])

        # Delete the extracted files
        logging.info("Deleting extracted files")
        shutil.rmtree(os.path.join(settings["gameLocation"], "LEGO"))
        return r
