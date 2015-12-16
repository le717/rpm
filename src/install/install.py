# -*- coding: utf-8 -*-


import os
import logging
import requests
from zipfile import ZipFile
from clint.textui import progress

from . import packagelist
from src.settings import user
from src.utils import legojam, utils


def main(package):
    # No value was given, silently no-op
    if package is None:
        return False

    # Get the user settings
    settings = user.UserSettings().load()

    # We do not have any settings
    if settings is None or not os.path.isdir(settings["lrPath"]):
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
    destZip = os.path.join(utils.AppUtils().cachePath,
                           "{0}.zip".format(package))
    with open(destZip, "wb") as f:
        total_length = int(r.headers.get("content-length"))
        for chunk in progress.bar(r.iter_content(chunk_size=1024),
                                  expected_size=(total_length / 1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()

    # Extract the JAM
    jamResult = legojam.main("extract")
    if not jamResult:
        logging.warning("There was an error extracting LEGO.JAM!")
        return False

    with ZipFile(destZip, "r") as z:
        # Get the package contents
        packageFiles = z.namelist()

        # The required package.json file is missing
        if "package.json" not in packageFiles:
            logging.warning("package.json not found!")
            print("Package is missing package.json and cannot be installed")
            return False

        # Remove the JSON from the archive so it is not extracted
        packageFiles.remove("package.json")

        # Install the package
        logging.info("Extracting archive")
        print("Installing package")
        z.extractall(settings["lrPath"], packageFiles)

    # Compress the JAM
    jamResult = legojam.main("build")
    if not jamResult:
        logging.warning("There was an error building LEGO.JAM!")
        return False

    # TODO Keep log of installed packages
    logging.info("Installation complete!")
    print("\nPackage {0} sucessfully installed".format(package))
    return True
