# -*- coding: utf-8 -*-
import os
import logging
import zipfile


TEST_FILES_ROOT_PATH = os.path.join(os.getcwd(), "tests", "files")
TEST_FILES_TEMP_PATH = os.path.join(TEST_FILES_ROOT_PATH, "temp")


def delete_temp_files():
    """Taken from Python docs.
    https://docs.python.org/3/library/os.html#os.walk
    """
    for root, dirs, files in os.walk(TEST_FILES_TEMP_PATH, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(TEST_FILES_TEMP_PATH)


def list_archive_files(zip):
    with zipfile.ZipFile(zip, "r") as z:
        return z.namelist()


def extract_archive(zip, path, f="all"):
    packageFiles = list_archive_files(zip)
    with zipfile.ZipFile(zip, "r") as z:
        if f == "all":
            z.extractall(path, packageFiles)
            return True
        else:
            if f not in packageFiles:
                return False
            else:
                z.extract(f, path)
                return True


def setUpClass():
    logging.disable(logging.ERROR)
    if not os.path.isdir(TEST_FILES_TEMP_PATH):
        os.makedirs(TEST_FILES_TEMP_PATH)
    else:
        delete_temp_files()


def tearDownClass():
    delete_temp_files()
