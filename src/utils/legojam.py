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

from src.settings import user as userSettings
from src.lib import JAMExtractor


def __extractJAM(path):
    """Helper function to extract the JAM archive.

    @param {String} path An absolute path to game installation.
    @returns {Boolean} True if extraction was successful, False otherwise.
    """
    return JAMExtractor.extract(os.path.join(path, "LEGO.JAM"), False)


def __buildJAM(path):
    """Helper function to build the JAM archive.

    @param {String} path An absolute path to game installation.
    @returns {Boolean} True if build was successful, False otherwise.
    """
    return JAMExtractor.build(os.path.join(path, "LEGO"), False)


def __findExtractedJam(path):
    """Find a possible pre-extracted JAM archive.

    @param {String} path An absolute path to game installation.
    @returns {Tuple.<boolean, ?string>} Index 0 will be False if no path
                                        was found. If True, index 1 will be
                                        the the path to the extracted files.
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
    settings = userSettings.load()

    # We do not have any settings
    if settings is None:
        logging.warning("User has not yet configured settings")
        print("You need to configure your settings before installing!")
        return False

    # This game release requires a JAM archive
    needsJam = (True if settings["gameRelease"] in (None, "1999") else False)

    # Find possible pre-extracted files
    preExtracted = __findExtractedJam(settings["gameLocation"])

    # File used to note if we extracted a JAM archive
    extractionIndicator = os.path.join(settings["gameLocation"], "extracted")

    # JAM extraction has been requested
    if action == "extract":
        # The JAM has already been extracted
        if preExtracted[0]:
            logging.info("LEGO.JAM has already been extracted")
            return preExtracted

        # The JAM needs to be extracted
        else:
            # Create the indicator file
            logging.info("Creating extracted files indicator")
            f = open(extractionIndicator, "xt")
            f.close()

            logging.info("Extracting LEGO.JAM")
            return (__extractJAM(settings["gameLocation"]),
                    os.path.join(settings["gameLocation"], "LEGO"))

    # JAM building has been requested
    elif action == "build":
        # We do not need a built JAM archive
        if not needsJam:
            logging.info("LEGO.JAM does not need building")

            # If we had extract the JAM despite not needing to rebuld it,
            # we still need to delete the indicator file
            if os.path.isfile(extractionIndicator):
                logging.info("Deleting extracted files indicator")
                os.remove(extractionIndicator)
            return True

        # We need a built JAM archive
        else:
            logging.info("Building LEGO.JAM")
            r = __buildJAM(settings["gameLocation"])

            # Delete the extracted files only if we created them
            if os.path.isfile(extractionIndicator):
                logging.info("Deleting extracted files indicator")
                os.remove(extractionIndicator)

                logging.info("Deleting extracted files")
                shutil.rmtree(os.path.join(settings["gameLocation"], "LEGO"))
            return r
