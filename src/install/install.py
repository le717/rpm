# -*- coding: utf-8 -*-
"""rpm - LEGO Racers mods package manager.

Created 2015-2017 Caleb Ely
<https://CodeTri.net/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
import logging
from zipfile import ZipFile
from clint.textui import colored

from . import packagelist
from src.settings import user as userSettings
from src.utils import download, legojam, utils
from src.validator import validator

__all__ = ("main")


def abort_install():
    """Abort a package installation.

    @return {Boolean} Always returns False.
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
    if not os.path.isdir(settings.get("gameLocation")):
        logging.warning("User has not yet configured settings")
        print(colored.red(
              "You need to configure your settings before installing!"))
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
    print("Package {0} is available for installation.".format(package))

    # Download the package
    destZip = os.path.join(appUtils.cachePath, "{0}.zip".format(package))
    r = download.toDisk(package,
                        availablePackages["packages"][package]["url"],
                        destZip)

    # Ensure the file was downloaded
    if not r:
        print(colored.red("Unable to download package {0}!".format(package)))
        return False

    # Extract the JAM
    jamResult, extractPath = legojam.extract()
    if not jamResult:
        logging.warning("There was an error extracting LEGO.JAM!")
        return False

    with ZipFile(destZip, "r") as z:
        # Get the package contents
        packageFiles = z.namelist()

        # The required package.json file is missing
        if not validator.hasPackageJson(packageFiles):
            logging.warning("package.json not found!")
            print(colored.red(
                  "Package is missing package.json and cannot be installed!"))
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
                return abort_install()

        # Remove the JSON from the archive so it is not extracted
        packageFiles.remove("package.json")

        # Install the package
        logging.info("Extracting package to {0}".format(extractPath))
        print("Installing package...")
        z.extractall(extractPath, packageFiles)

    # Compress the JAM
    jamResult = legojam.build()
    if not jamResult:
        logging.warning("There was an error building LEGO.JAM!")
        return False

    # TODO Keep log of installed packages
    logging.info("Installation complete!")
    print("\nPackage {0} sucessfully installed.".format(package))
    return True
