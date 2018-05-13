# -*- coding: utf-8 -*-
"""rpm - LEGO Racers mods package manager.

Created 2015-2018 Caleb Ely
<https://CodeTri.net/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
import logging
from src.utils import jsonutils
from src.validator import validator

__all__ = ("main", "create_package_fols")


def __display_error(value: str, message: str):
    """Display a validation error message.

    @param {String} value The invalid value in question.
    @param {String} message The error message.
    """
    logging.warning(f"Invalid package value: {value}")
    logging.debug(f"Reason: {message}")
    print(message)


def __get_package_loc() -> str:
    """Get the package location.

    @return {String}
    """
    default_loc = os.getcwd()
    valid_loc = False

    while not valid_loc:
        print("Package output location (leave blank for current directory)")
        package_loc = input(f"location: ({default_loc}) ")
        # The default value will be used
        if package_loc == "":
            package_loc = default_loc

        # We need to validate the package name
        package_loc = os.path.abspath(package_loc)
        r = validator.validate_location(package_loc)

        # Display error message if needed
        if r["result"] is None:
            valid_loc = True
        else:
            __display_error(r["value"], r["message"])
    return package_loc


def __get_package_name(loc: str) -> str:
    """Get the package name.

    @param {String} loc - The package output location.
    @return {String}
    """
    default_name = os.path.basename(loc)
    valid_name = False

    while not valid_name:
        package_name = input(f"name: ({default_name}) ")
        # The default value will be used
        if package_name == "":
            package_name = default_name

        # Display error message if needed
        r = validator.validate_name(package_name)
        if r["result"] is None:
            valid_name = True
        else:
            __display_error(r["value"], r["message"])
    return package_name


def __get_package_version() -> str:
    """Get the package version.

    @return {String}
    """
    default_version = "1.0.0"
    valid_version = False

    while not valid_version:
        package_version = input(f"version: ({default_version}) ")
        # The default value will be used
        if package_version == "":
            package_version = default_version
            break

        # Display error message if needed
        r = validator.validate_version(package_version)
        if r["result"] is None:
            valid_version = True
        else:
            __display_error(r["value"], r["message"])
    return package_version


def create_package_fols(path: str) -> bool:
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


def main(*args) -> bool:
    print("""This process will walk you through creating a new package.
It tries to suggest sensible default when available.

Press <Ctrl+c> at any time to abort.
""")

    try:
        package_details = {
            "name": None,
            "version": None,
            "author": None,
            "description": None,
            "homepage": None
        }

        # Get the package loc, name, and version
        logging.info("Collecting package location")
        package_loc = __get_package_loc()
        logging.info("Collecting package name")
        package_details["name"] = __get_package_name(package_loc)
        logging.info("Collecting package version")
        package_details["version"] = __get_package_version()

        # Get the remaining package details
        logging.info("Collecting remaining package details")
        package_details["author"] = input("author: ")
        package_details["description"] = input("description: ")
        package_details["homepage"] = input("homepage: ")

        # Write package.json
        logging.info("Writing package.json")
        package_json = os.path.join(package_loc, "package.json")
        # TODO Handle failing to write file
        jsonutils.write(package_json, package_details, 4)

        # Create the required folder structure
        create_package_fols(package_loc)

        print(f"""
Boilerplate for package {package_details['name']} successfully created.""")
        return True

    # The user canceled the processed
    except KeyboardInterrupt:
        logging.info("User canceled package creation.")
        print("\nPackage creation canceled.")
        return False
