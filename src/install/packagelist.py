# -*- coding: utf-8 -*-


import logging
import requests

from src.settings import app


def main():
    url = app.AppSettings().load()["baseUrl"]

    # Fetch the request from the server
    r = requests.get("{0}/package-list.json".format(url))
    if r.status_code == requests.codes.ok:
        logging.info("Package list sucessfully downloaded")
        return r.json()

    # We were unable to fetch the package list
    logging.warning("Unable to download package list!")
    print("""We were unable to download the package list at this time.
Please try again later.""")
    return None
