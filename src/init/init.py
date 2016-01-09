# -*- coding: utf-8 -*-
"""pire - LEGO Racers mods package manager.

Created 2015 Caleb Ely
<http://codetriangle.me/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
import logging
from src.utils import jsonutils
from src.validator import validator


def main(*args):
    print("""This utility will walk you through creating a package.json file.
It only covers the most common items, and tries to guess sensible defaults.

Press ^C at any time to quit.
""")

    try:
        packageDetails = {
            "name": None,
            "version": None,
            "author": None,
            "description": None,
            "homepage": None
            }

        # Get the package name
        logging.info("Collecting package name")
        defaultName = os.path.basename(os.getcwd())
        validName = False

        while not validName:
            packageName = input("name: ({0}) ".format(defaultName))
            # The default value will be used
            if packageName == "":
                packageName = defaultName

            # We still need to validate both a user-supplied name
            # and the default name
            result = validator.validateName(packageName)

            # Display error message if needed
            if not result[0]:
                logging.warning("Invalid package name {0}!".format(
                                packageName))
                logging.debug("Reason: {0}".format(result[1]))
                print(result[1])
            validName = result[0]

        # Store the package name
        packageDetails["name"] = packageName

        # Get the package version
        logging.info("Collecting package version")
        validVersion = False

        while not validVersion:
            packageVersion = input("version: (1.0.0) ")
            # The default value will be used
            if packageVersion == "":
                break
            result = validator.validateVersion(packageVersion)

            # Display error message if needed
            if not result[0]:
                logging.warning("Invalid package version {0}!".format(
                                packageVersion))
                logging.debug("Reason: {0}".format(result[1]))
                print(result[1])
            validVersion = result[0]

        # Store the package version
        packageDetails["version"] = (packageVersion if packageVersion
                                     else "1.0.0")

        # Get the remaining package details
        logging.info("Collecting remaining package details")
        packageDetails["author"] = input("author: ")
        packageDetails["description"] = input("description: ")
        packageDetails["homepage"] = input("homepage: ")

        # Write package.json
        logging.info("Writing package.json")
        packageJson = os.path.join(os.getcwd(), "package.json")
        jsonutils.write(packageJson, packageDetails, 4)

        # Create the required folder structure
        logging.info("Creating folders")
        folders = (os.path.join(os.getcwd(), "MENUDATA"),
                   os.path.join(os.getcwd(), "GAMEDATA"))
        for fol in folders:
            if not os.path.isdir(fol):
                os.makedirs(fol)

        print("\nBoilerplate for package {0} sucessfully created.".format(
              packageDetails["name"]))
        return True

    # The user canceled the processed
    except KeyboardInterrupt:
        logging.info("User canceled package creation.")
        print("\nPackage creation canceled.")
        return False
