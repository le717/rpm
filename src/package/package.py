# -*- coding: utf-8 -*-
"""rpm - LEGO Racers mods package manager.

Created 2015-2018 Caleb Ely
<https://CodeTri.net/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
import logging
from zipfile import ZIP_DEFLATED, ZipFile, is_zipfile

from src.utils import jsonutils, utils

__all__ = ("main")


def main(directory: str) -> bool:
    """TODO.

    @param {String} directory - The directory to package.
                                Package files should be located here.
    @return {Boolean} True if the process was successful, False otherwise.
    """
    # No package directory was given
    if directory is None:
        logging.warning("No directory was specified!")
        utils.display_message({
            "result": "error",
            "message": "No directory was specified for packaging!"
        })
        return False

    # The given directory does not exist
    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        logging.warning("Directory specified does not exist!")
        utils.display_message({
            "result": "error",
            "message": "The directory specified could not be found!"
        })
        return False

    # Make sure we have a package.json file
    if not os.path.isfile(os.path.join(directory, "package.json")):
        logging.warning("package.json not found!")
        utils.display_message({
            "result": "error",
            "message": "File package.json is missing. Packaging cannot proceed!"
        })
        return False

    # Generate the package file name, repacing verison dots with dashes
    # to eliminate potentionally ambiguous Windows file type identification
    package_details = jsonutils.read(os.path.join(directory, "package.json"))
    package_archive_name = "{}-v{}.zip".format(
        package_details["name"],
        package_details["version"].replace(".", "-")
    )
    package_archive_loc = os.path.join(directory, package_archive_name)

    # Generate a listing of the package's files
    package_files = []
    filtered_files = ("thumbs.db", "ethumbs.db", "desktop.ini")
    for root, dirs, files in os.walk(directory):
        for f in files:
            # Perform super basic file filtering
            if f.lower() in filtered_files:
                continue

            # Because we are compressing a directory that is not
            # the current directory, we need to construct both the
            # absolute and relative path for the individual files
            # to preserve the folder/file structure.
            # We also disrgard all empty folders from packaging
            # because there is no need to package an empty folder
            abs_path = os.path.join(root, f)
            package_files.append({
                "abs_path": abs_path,
                "rel_path": abs_path.replace(f"{directory}{os.path.sep}", "")
            })

    # Compress all files into a zip archive
    with ZipFile(package_archive_loc, "w", compression=ZIP_DEFLATED) as zf:
        for f in package_files:
            zf.write(f["abs_path"], f["rel_path"])

    # For some reason, packaging failed
    # TODO Likely need a try...catch here
    if not is_zipfile(package_archive_loc):
        return False
    return True
