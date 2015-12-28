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
    @returns {@todo|Boolean} @todo
    """
    try:
        # Make sure it exists
        if not os.path.isfile(path):
            logging.warning("Cannot find JSON file {0}".format(path))
            return False

        # Read and parse the file
        logging.info("Reading JSON file {0}".format(path))
        with open(path, "rt", encoding="utf-8") as f:
            data = json.load(f)
        return data

    # The file is not valid JSON, sliently fail
    except ValueError:
        logging.warning("Cannot parse JSON file {0}".format(path))
        return False


def write(path, data):
    """Write a JSON file to disk.

    @todo Implement this function!

    @param {String} path An absolute path to the JSON file to be written.
    @param {String} data The data to be written.
    @returns {@todo} @todo
    """
    pass
