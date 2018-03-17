# -*- coding: utf-8 -*-
"""rpm - LEGO Racers mods package manager.

Created 2015-2018 Caleb Ely
<https://CodeTri.net/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
import json
import logging


def read(path):
    """Read and parse a JSON file from disk.

    @param {String} path An absolute path to the JSON file to be read.
    @return {*|NoneType} The parsed JSON data,
                        None if file could not be loaded or parsed.
    """
    try:
        # Make sure it exists
        if not os.path.isfile(path):
            logging.warning(f"Cannot find JSON file {path}")
            return None

        # Read and parse the file
        logging.info(f"Reading JSON file {path}")
        with open(path, "rt", encoding="utf-8") as f:
            data = json.load(f)
        return data

    # The file is not valid JSON, sliently fail
    except json.JSONDecodeError as e:
        logging.warning(f"Cannot parse JSON file {path}")
        logging.debug(e)
        return None


def write(path, data, indent=None):
    """Write a JSON file to disk.

    @param {String} path An absolute path to the JSON file to be written.
    @param {*} data The JSON-parsable data to be written.
    @param {Integer} [indent=None] Indentation level of resulting file.
    @return {Boolean} True if successfully written, False otherwise.
    """
    try:
        with open(path, "wt", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=indent, sort_keys=True))
            logging.info(f"JSON file {path} successfully written")
        return True

    # Silently fail
    except PermissionError:
        logging.warning(f"JSON file {path} could not be written!")
        return False
