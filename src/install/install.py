# -*- coding: utf-8 -*-
"""rpm - LEGO Racers mods package manager.

Created 2015-2018 Caleb Ely
<https://CodeTri.net/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
import logging
from zipfile import ZipFile
from clint.textui import colored

from src.settings import user
from src.utils import legojam, utils
from src.validator import validator

__all__ = ("main")


def display_message(error):
    # Determine the proper color to use
    # Red for errors, yellow for warnings
    color = (colored.red if error["result"] == "error"
             else colored.yellow)
    print(color(f"{error['result'].capitalize()}: {error['message']}", bold=True))

    # If this is an error, we'll need to abort the process
    # once all errors are reported
    if error["result"] == "error":
        return True
    return False


def abort_install():
    """Abort a package installation.

    @return {Boolean} Always returns False.
    """
    logging.info("Installation aborted")
    print("Installation will now abort.")
    return False


def main(package):
    # No package was given
    if package is None:
        logging.warning("No package was specified!")
        print(colored.red("No package was specified for installation."))
        return False

    # The package path given does not exist
    package = os.path.abspath(package)
    if not os.path.isfile(package):
        logging.warning("Package specified does not exist!")
        print(colored.red("The package specified could not be found."))
        return False

    # Get the settings
    settings = user.load()
    app_utils = utils.AppUtils()

    # We do not have any settings
    if not os.path.isdir(settings.get("gameLocation")):
        logging.warning("User has not yet configured settings!")
        print(colored.red(
              "You need to configure your settings before installing!"))
        return False

    # Extract the JAM
    jam_result, extract_path = legojam.extract()
    if not jam_result:
        logging.warning("There was an error extracting LEGO.JAM!")
        return False

    with ZipFile(package, "r") as z:
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
        validate_result = validator.packageJson(
            os.path.join(app_utils.tempPath, "package.json"))

        # Validation errors occurred
        if validate_result:
            logging.warning("package.json validation errors occurred!")
            print("\nThe following errors in package.json were found:")

            # Display each validation error message
            should_abort = False
            for error in validate_result:
                should_abort = display_message(error)

            # A fatal error occurred, we cannot continue on
            if should_abort:
                return abort_install()

        # Remove the JSON from the archive so it is not extracted
        files.remove("package.json")

        # Install the package
        logging.info(f"Extracting package to {extract_path}")
        print("Installing package...")
        z.extractall(extract_path, files)

    # Compress the JAM
    jam_result = legojam.build()
    if not jam_result:
        logging.warning("There was an error building LEGO.JAM!")
        return False

    # TODO Keep log of installed packages
    logging.info("Installation complete!")
    print(f"\nPackage {package} sucessfully installed.")
    return True
