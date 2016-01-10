# -*- coding: utf-8 -*-
"""pire - LEGO Racers mods package manager.

Created 2015 Caleb Ely
<http://codetriangle.me/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
import json
import logging


def read(path):
    """Read and parse a JSON file from disk.

    @param {String} path An absolute path to the JSON file to be read.
    @returns {*|NoneType} The parsed JSON data,
                        None if file could not be loaded or parsed.
    """
    # Python 3.5+ uses a new exception for JSON errors
    try:
        parseException = json.JSONDecodeError
    except AttributeError:
        parseException = ValueError

    try:
        # Make sure it exists
        if not os.path.isfile(path):
            logging.warning("Cannot find JSON file {0}".format(path))
            return None

        # Read and parse the file
        logging.info("Reading JSON file {0}".format(path))
        with open(path, "rt", encoding="utf-8") as f:
            data = json.load(f)
        return data

    # The file is not valid JSON, sliently fail
    except parseException as e:
        logging.warning("Cannot parse JSON file {0}".format(path))
        logging.debug(e)
        return None


def write(path, data, indent=None):
    """Write a JSON file to disk.

    @param {String} path An absolute path to the JSON file to be written.
    @param {*} data The JSON-parsable data to be written.
    @param {Integer} [indent=None] Indentation level of resulting file.
    @returns {Boolean} True if successfully written, False otherwise.
    """
    try:
        with open(path, "wt", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=indent, sort_keys=True))
            logging.info("JSON file {0} successfully written".format(path))
        return True

    # Silently fail
    except PermissionError:
        logging.warning("JSON file {0} could not be written!".format(path))
        return False
