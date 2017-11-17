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


def display_message(error):
    result = False

    # Determine the proper color to use
    # Red for errors, yellow for warnings
    color = (colored.red if error["result"] == "error"
             else colored.yellow)
    print(color("{0}: {1}".format(
            error["result"].capitalize(),
            error["message"]
            ), bold=True))

    # If this is an error, we'll need to abort the process
    # once all errors are reported
    if error["result"] == "error":
        result = True
    return result


def abort_install():
    """Abort a package installation.

    @return {Boolean} Always returns False.
    """
    logging.info("Installation aborted")
    print("Installation will now abort.")
    return False


def main(package):
    # No value was given, silently no-op
    if package is None:
        return False

    # Get the user settings
    settings = userSettings.load()
    app_utils = utils.AppUtils()

    # We do not have any settings
    if not os.path.isdir(settings.get("gameLocation")):
        logging.warning("User has not yet configured settings")
        print(colored.red(
              "You need to configure your settings before installing!"))
        return False

    # Fetch the package list
    available_packages = packagelist.main()

    # We were unable to fetch the package list
    if available_packages is None:
        return False

    # The desired package is not available
    if package not in available_packages["packages"].keys():
        logging.warning("Cannot find package {0}!".format(package))
        print("Unable to find package {0} for installation!".format(package))
        return None

    # The package was found
    logging.info("Package {0} is available".format(package))
    print("Package {0} is available for installation.".format(package))

    # Download the package
    dest = os.path.join(app_utils.cachePath, "{0}.zip".format(package))
    r = download.toDisk(package,
                        available_packages["packages"][package]["url"],
                        dest)

    # Ensure the file was downloaded
    if not r:
        print(colored.red("Unable to download package {0}!".format(package)))
        return False

    # Extract the JAM
    jam_result, extract_path = legojam.extract()
    if not jam_result:
        logging.warning("There was an error extracting LEGO.JAM!")
        return False

    with ZipFile(dest, "r") as z:
        # Get the package contents
        files = z.namelist()

        # The required package.json file is missing
        if not validator.hasPackageJson(files):
            logging.warning("package.json not found!")
            print(colored.red(
                  "Package is missing package.json and cannot be installed!"))
            return False

        # Extract and validate package.json
        z.extract("package.json", app_utils.tempPath)
        validateResult = validator.packageJson(
            os.path.join(app_utils.tempPath, "package.json"))

        # Validation errors occurred
        if validateResult:
            logging.warning("package.json validation errors occurred!")
            print("\nThe following errors in package.json were found:")

            # Display each validation error message
            should_abort = False
            for error in validateResult:
                should_abort = display_message(error)

            # A fatal error occurred, we cannot continue on
            if should_abort:
                return abort_install()

        # Remove the JSON from the archive so it is not extracted
        files.remove("package.json")

        # Install the package
        logging.info("Extracting package to {0}".format(extract_path))
        print("Installing package...")
        z.extractall(extract_path, files)

    # Compress the JAM
    jam_result = legojam.build()
    if not jam_result:
        logging.warning("There was an error building LEGO.JAM!")
        return False

    # TODO Keep log of installed packages
    logging.info("Installation complete!")
    print("\nPackage {0} sucessfully installed.".format(package))
    return True
