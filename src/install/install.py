# -*- coding: utf-8 -*-
"""rpm - LEGO Racers mods package manager.

Created 2015-2016 Caleb Ely
<http://codetriangle.me/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
import logging
import requests
from zipfile import ZipFile
from clint.textui import progress, colored

from . import packagelist
from src.settings import user as userSettings
from src.utils import legojam, utils
from src.validator import validator

__all__ = ("main")


def abortInstall():
    """@todo.

    @returns {Boolean} Always returns False.
    """
    logging.info("Installation aborted")
    print("Installation will now abort")
    return False


def main(package):
    # No value was given, silently no-op
    if package is None:
        return False

    # Get the user settings
    settings = userSettings.load()
    appUtils = utils.AppUtils()

    # We do not have any settings
    if settings is None or not os.path.isdir(settings["gameLocation"]):
        logging.warning("User has not yet configured settings")
        print("You need to configure your settings before installing!")
        return False

    # Fetch the package list
    availablePackages = packagelist.main()

    # We were unable to fetch the package list
    if availablePackages is None:
        return False

    # The desired package is not available
    if package not in availablePackages["packages"].keys():
        logging.warning("Cannot find package {0}!".format(package))
        print("Unable to find package {0} for installation!".format(package))
        return None

    # The package was found
    logging.info("Package {0} is available".format(package))
    print("Package {0} is available for installation".format(package))

    # Download the package
    print("Downloading package {0}".format(package))
    r = requests.get(availablePackages["packages"][package]["url"],
                     stream=True)

    # Write the package to disk
    # Sourced from http://stackoverflow.com/a/20943461
    destZip = os.path.join(appUtils.cachePath, "{0}.zip".format(package))
    with open(destZip, "wb") as f:
        total_length = int(r.headers.get("content-length"))
        for chunk in progress.bar(r.iter_content(chunk_size=1024),
                                  expected_size=(total_length / 1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()

    # Extract the JAM
    jamResult, extractPath = legojam.main("extract")
    if not jamResult:
        logging.warning("There was an error extracting LEGO.JAM!")
        return False

    with ZipFile(destZip, "r") as z:
        # Get the package contents
        packageFiles = z.namelist()

        # The required package.json file is missing
        if not validator.hasPackageJson(packageFiles):
            logging.warning("package.json not found!")
            print("Package is missing package.json and cannot be installed")
            return False

        # Extract and validate package.json
        z.extract("package.json", appUtils.tempPath)
        validateResult = validator.packageJson(
            os.path.join(appUtils.tempPath, "package.json"))

        # Validation errors occurred
        if validateResult:
            logging.warning("package.json validation errors occurred!")
            print("\nThe following errors in package.json were found:")

            shouldAbort = False
            for error in validateResult:
                # Issue a warning
                if error["result"] == "warning":
                    print(colored.yellow("Warning: {0}".format(
                          error["message"]), bold=True))

                # Issue an error
                elif error["result"] == "error":
                    shouldAbort = True
                    print(colored.red("Error: {0}".format(
                          error["message"]), bold=True))

            # A fatal error occurred, we cannot continue on
            if shouldAbort:
                return abortInstall()

        # Remove the JSON from the archive so it is not extracted
        packageFiles.remove("package.json")

        # Install the package
        logging.info("Extracting package to {0}".format(extractPath))
        print("Installing package")
        z.extractall(extractPath, packageFiles)

    # Compress the JAM
    jamResult = legojam.main("build")
    if not jamResult:
        logging.warning("There was an error building LEGO.JAM!")
        return False

    # TODO Keep log of installed packages
    logging.info("Installation complete!")
    print("\nPackage {0} sucessfully installed".format(package))
    return True
