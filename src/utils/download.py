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
from clint.textui import progress

__all__ = ("toDisk", "toMemory")


def toDisk(name, url, dest):
    """Download a file and save it to disk.

    @param {String} name The pretty name of the desired file.
    @param {String} url The URL to the file.
    @param {String} dest The destination path and file name for the file.
    @returns {Boolean} True if file was successfully downloaded,
                       False otherwise.
    """
    # Download the package
    print("Downloading {0}".format(name))
    r = requests.get(url, stream=True)

    # The file could not be fetched
    if r.status_code != requests.codes.ok:
        logging.error("{0} could not be downloaded!".format(url))
        return False

    # Write the downloaded file to disk
    # Sourced from http://stackoverflow.com/a/20943461
    with open(dest, "wb") as f:
        total_length = int(r.headers.get("content-length"))
        for chunk in progress.bar(r.iter_content(chunk_size=1024),
                                  expected_size=(total_length / 1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()

    # Confirm the file was downloaded
    return os.path.isfile(dest)


def toMemory(url):
    """Download a file but do not write it to disk.

    @param {String} url The URL to the file.
    return {Boolean|Requests} A requests object if the file was downloaded,
                              False otherwise.
    """
    r = requests.get(url, stream=True)
    if r.status_code == requests.codes.ok:
        logging.info("{0} sucessfully downloaded".format(url))
        return r
    return False
