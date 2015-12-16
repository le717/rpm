# -*- coding: utf-8 -*-


import os
import shutil
import logging

from src.settings import user
from src.lib import JAMExtractor


def main(action):
    # Get the user settings
    settings = user.UserSettings().load()

    # We do not have any settings
    if settings is None:
        logging.warning("User has not yet configured settings")
        print("You need to configure your settings before installing!")
        return False

    # We need to only extract/build when release is 1999 or N/A
    shouldAct = (True if settings["lrVer"] in ("1999", None) else False)

    # Perform the desired action
    if action == "extract" and shouldAct:
        logging.info("Extracting LEGO.JAM")
        return JAMExtractor.extract(os.path.join(
            settings["lrPath"], "LEGO.JAM"), False)

    elif action == "build" and shouldAct:
        logging.info("Building LEGO.JAM")
        r = JAMExtractor.build(os.path.join(
            settings["lrPath"], "LEGO"), False)

        # Delete the extracted files
        logging.info("Deleting extracted files")
        shutil.rmtree(os.path.join(settings["lrPath"], "LEGO"))
        return r
