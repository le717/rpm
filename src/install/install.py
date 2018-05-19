# -*- coding: utf-8 -*-
"""rpm - LEGO Racers mods package manager.

Created 2015-2018 Caleb Ely
<https://CodeTri.net/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
import logging
from zipfile import ZipFile, is_zipfile
from clint.textui import colored

from src.settings import user
from src.utils import legojam, jsonutils, utils
from src.validator import validator

__all__ = ("main")


def __display_message(error: dict) -> bool:
    # Determine the proper color to use
    # Red for errors, yellow for warnings
    color = (colored.red if error["result"] == "error"
             else colored.yellow)
    print(color(
        f"{error['result'].capitalize()}: {error['message']}",
        bold=True
    ))

    # If this is an error, we'll need to abort the process
    # once all errors are reported
    if error["result"] == "error":
        return True
    return False


def __abort_install() -> bool:
    """Abort a package installation.

    @return {Boolean} Always returns False.
    """
    logging.info("Installation aborted")
    print("Installation will now abort.")
    return False


def main(package) -> bool:
    settings = user.load()
    app_utils = utils.AppUtils()
    package_details = None

    # We do not have a set game location
    if not os.path.isdir(settings.get("gameLocation")):
        logging.warning("User has not yet configured settings!")
        __display_message({
            "result": "error",
            "message": "You need to configure your settings before installing!"
        })
        return False

    # No package was given
    if package is None:
        logging.warning("No package was specified!")
        __display_message({
            "result": "error",
            "message": "No package was specified for installation!"
        })
        return False

    # The package path given does not exist or is not a valid zip
    package = os.path.abspath(package)
    if not is_zipfile(package):
        logging.warning("Package specified is not a valid archive!")
        __display_message({
            "result": "error",
            "message": "The file specified is not a valid package!"
        })
        return False

    # Extract the JAM
    # TODO This fails in most cases,
    # need to fix legojam module return values
    r = legojam.extract()
    jam_result = r["result"]
    extract_path = r["path"]
    if not jam_result:
        # TODO Tell the user what happened
        logging.warning("There was an error extracting LEGO.JAM!")
        return False

    # Getting ready to install the package
    package_files = []
    with ZipFile(package, "r") as zf:
        package_files = zf.namelist()

        # The required package.json file is missing
        if not validator.has_package_json(package_files):
            logging.warning("File package.json not found!")
            __display_message({
                "result": "error",
                "message": "Package is missing package.json and cannot be installed!"
            })
            return False

        # Extract and validate package.json
        zf.extract("package.json", app_utils.temp_path)
        validate_result = validator.package_json(
            os.path.join(app_utils.temp_path, "package.json"))

        # Validation errors occurred
        # TODO Does this need to occur here or in package task?
        if validate_result:
            logging.warning("package.json validation errors occurred!")
            print("\nThe following package.json errors were found:")

            # Display each validation error message
            should_abort = False
            for error in validate_result:
                should_abort = __display_message(error)

            # A fatal error occurred, we cannot continue on
            if should_abort:
                return __abort_install()

        # Get the package details before removing the JSON
        # from the archive listing so it is not extracted
        package_details = jsonutils.read(
            os.path.join(app_utils.temp_path, "package.json"))
        package_files.remove("package.json")

        # Install the package
        logging.info(f"Extracting package to {extract_path}")
        print("Installing package...")
        zf.extractall(extract_path, package_files)

    # Compress the JAM
    jam_result = legojam.build()
    if not jam_result:
        # TODO Tell the user what happened
        logging.warning("There was an error building LEGO.JAM!")
        return False

    # TODO Keep persistent log of installed packages and files
    logging.info("Installation complete!")
    print("{0} {1} sucessfully installed.".format(
        package_details['name'], package_details['version']
    ))
    return True
