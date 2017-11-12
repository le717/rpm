# -*- coding: utf-8 -*-
"""rpm - LEGO Racers mods package manager.

Created 2015-2017 Caleb Ely
<https://CodeTri.net/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
import logging
from src.utils import jsonutils
from src.validator import validator

__all__ = ("main", "createPackageFols")


def __displayError(value, message):
    """Display a validation error message.

    @param {String} value The invalid value in question.
    @param {String} message The error message.
    """
    logging.warning("Invalid package value: {0}".format(value))
    logging.debug("Reason: {0}".format(message))
    print(message)


def __getPackageName():
    """Get the package name.

    @return {String}
    """
    defaultName = os.path.basename(os.getcwd())
    validName = False

    while not validName:
        packageName = input("name: ({0}) ".format(defaultName))
        # The default value will be used
        if packageName == "":
            packageName = defaultName

        # We still need to validate both a user-supplied name
        # and the default name
        r = validator.validateName(packageName)

        # Display error message if needed
        if r["result"] is None:
            validName = True
        else:
            __displayError(r["value"], r["message"])
    return packageName


def __getPackageVersion():
    """Get the package version.

    @return {String}
    """
    validVersion = False

    while not validVersion:
        packageVersion = input("version: (1.0.0) ")
        # The default value will be used
        if packageVersion == "":
            break
        r = validator.validateVersion(packageVersion)

        # Display error message if needed
        if r["result"] is None:
            validVersion = True
        else:
            __displayError(r["value"], r["message"])
    return (packageVersion if packageVersion else "1.0.0")


def createPackageFols(path):
    """Create the package folder structure.

    @param {String} path An absolute path to the package location.
    @return {Boolean} Always returns True.
    """
    logging.info("Creating folders")
    folders = (os.path.join(path, "MENUDATA"),
               os.path.join(path, "GAMEDATA"))
    for fol in folders:
        if not os.path.isdir(fol):
            os.makedirs(fol)
    return True


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

        # Get the package name and version
        logging.info("Collecting package name")
        packageDetails["name"] = __getPackageName()
        logging.info("Collecting package version")
        packageDetails["version"] = __getPackageVersion()

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
        createPackageFols(os.getcwd())

        print("\nBoilerplate for package {0} sucessfully created.".format(
              packageDetails["name"]))
        return True

    # The user canceled the processed
    except KeyboardInterrupt:
        logging.info("User canceled package creation.")
        print("\nPackage creation canceled.")
        return False
