# -*- coding: utf-8 -*-
"""rpm - LEGO Racers mods package manager.

Created 2015-2018 Caleb Ely
<https://CodeTri.net/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
import shutil
import logging
import distutils.dir_util
from clint.textui import colored

from src.lib import JAMExtractor
from src.settings import user as userSettings
from src.utils import utils

__all__ = ("build", "config_2001_copy", "extract")


def __extract_jam(path):
    """Helper function to extract the JAM archive.

    @param {String} path An absolute path to game installation.
    @return {Boolean} True if extraction was successful, False otherwise.
    """
    logging.info("Extracting LEGO.JAM")
    return JAMExtractor.extract(os.path.join(path, "LEGO.JAM"), False)


def __build_jam(path):
    """Helper function to build the JAM archive.

    @param {String} path An absolute path to game installation.
    @return {Boolean} True if build was successful, False otherwise.
    """
    logging.info("Building LEGO.JAM")
    return JAMExtractor.build(os.path.join(path, "LEGO"), False)


def __find_extracted_jam(path):
    """Find a possible pre-extracted JAM archive.

    @param {String} path An absolute path to game installation.
    @return {Tuple.<boolean, ?string>} Index 0 will be False if no path
                                        was found. If True, index 1 will be
                                        the the path to the extracted files.
    """
    results = (False,)
    extracted_paths = (
        (os.path.join(path, "MENUDATA"),
         os.path.join(path, "GAMEDATA")),
        (os.path.join(path, "LEGO", "MENUDATA"),
         os.path.join(path, "LEGO", "GAMEDATA"))
    )

    # The MENUDATA/GAMEDATA folders already exist
    for path_group in extracted_paths:
        if os.path.isdir(path_group[0]) and os.path.isdir(path_group[1]):
            # Get the exact path detected
            extracted_path = (path if extracted_paths.index(path_group) == 0
                              else os.path.join(path, "LEGO"))
            results = (True, extracted_path)
            break

    return results


def config_2001_copy(path):
    """
    Configure a 2001 game release to run without a JAM archive,
    as explained on the following website:
    http://www.rockraidersunited.com/topic/7178-the-2001-version-loads-gamedata-menudata-folders-if-an-emtpy-valid-legojam-file-is-present/
    """
    # If the JAM has already been extracted, we have nothing to do here
    logging.info("Check if we even need to configure the game")
    if __find_extracted_jam(path)[0]:
        return True

    # Extract the JAM
    jam_result = __extract_jam(path)
    if not jam_result:
        logging.warning("There was an error extracting LEGO.JAM!")
        return False

    # Copy the extracted files to their proper location
    print("\nPerforming configuration...")
    logging.info("Copy the extracted files to their proper location")
    distutils.dir_util.copy_tree(os.path.join(path, "LEGO"), path)
    distutils.dir_util.remove_tree(os.path.join(path, "LEGO"))

    # Rename the existing JAM archive and grab our dummy archive
    logging.info("Backup the existing JAM and add our dummy file in its place")
    os.rename(os.path.join(path, "LEGO.JAM"),
              os.path.join(path, "PRE-RPM-LEGO.JAM"))
    shutil.copy2(os.path.join(utils.AppUtils().config_path, "LEGO.JAM"),
                 os.path.join(path, "LEGO.JAM"))
    return True


def __main(action):
    # Get the user settings
    settings = userSettings.load()

    # We do not have any settings
    if settings.get_all() is None:
        logging.warning("User has not yet configured settings")
        print(colored.red(
              "You need to configure your settings before installing!"))
        return False

    # This game release requires a JAM archive
    needs_jam = (True if settings.get("gameRelease") is None else False)

    # Find possible pre-extracted files
    pre_extracted = __find_extracted_jam(settings.get("gameLocation"))

    # File used to note if we extracted a JAM archive
    indicator = os.path.join(settings.get("gameLocation"), "extracted")

    # JAM extraction has been requested
    if action == "extract":
        # The JAM has already been extracted
        if pre_extracted[0]:
            logging.info("LEGO.JAM has already been extracted")
            return pre_extracted

        # The JAM needs to be extracted
        else:
            # Create the indicator file
            logging.info("Creating extracted files indicator")
            f = open(indicator, "xt")
            f.close()

            # Extract the JAM
            return (__extract_jam(settings.get("gameLocation")),
                    os.path.join(settings.get("gameLocation"), "LEGO"))

    # JAM building has been requested
    elif action == "build":
        # We do not need a built JAM archive
        if not needs_jam:
            logging.info("LEGO.JAM does not need building")

            # If we had extract the JAM despite not needing to rebuld it,
            # we still need to delete the indicator file
            if os.path.isfile(indicator):
                logging.info("Deleting extracted files indicator")
                os.remove(indicator)
            return True

        # We need a built JAM archive
        else:
            r = __build_jam(settings.get("gameLocation"))

            # Delete the extracted files only if we created them
            if os.path.isfile(indicator):
                logging.info("Deleting extracted files indicator")
                os.remove(indicator)

                logging.info("Deleting extracted files")
                shutil.rmtree(
                    os.path.join(settings.get("gameLocation"), "LEGO")
                )
            return r


def build():
    return __main("build")


def extract():
    return __main("extract")
