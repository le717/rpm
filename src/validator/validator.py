# -*- coding: utf-8 -*-
"""pire - LEGO Racers mods package manager.

Created 2015 Caleb Ely
<http://codetriangle.me/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import re
import logging
from clint.textui import colored
from src.utils import jsonutils

__all__ = ("validateName", "validateVersion", "hasPackageJson", "packageJson")


def __makeErrorDict(value, result, message):
    """Create an error dictionary.

    @param {*} value The value in question that caused the error.
    @param {*} result The error status.
    @param {*} message The error message.
    @returns {Dictionary.<value, result, message>} An error dictionary.
                                                   Keys are same as params.
    """
    return {
        "message": message,
        "result": result,
        "value": value
    }


def validateName(name):
    """Validate the package name.

    @param {String} name The package name.
    @returns {Dictionary} See signature for private __makeErrorDict method.
    """
    name = name.strip()
    # Empty name
    if name == "":
        return __makeErrorDict(name, False, "The name cannot be empty.")

    # Leading dot/underscore check
    if name[0] == ".":
        return __makeErrorDict(name, False,
                               "The name cannot start with a period.")
    if name[0] == "_":
        return __makeErrorDict(name, False,
                               "The name cannot start with an underscore.")

    # Spaces check
    if re.findall(r"\s", name):
        return __makeErrorDict(name, False,
                               "The name cannot contain spaces.")

    # Length check
    if len(name) > 214:
        return __makeErrorDict(name, False,
                               "The name cannot contain more than 214"
                               " characters.")

    # Uppercase letter check
    if re.findall(r"[A-Z]", name):
        return __makeErrorDict(name, False,
                               "The name cannot contain capital letters.")

    badChars = ("\\", "/", ":", "*", "?", '"', "<", ">", "|")
    badNames = ("aux", "com1", "com2", "com3", "com4", "con",
                "lpt1", "lpt2", "lpt3", "prn", "nul")

    # Invalid Windows names/charcters check
    if name in badNames:
        return __makeErrorDict(name, False,
                               'Name "{0}" is not allowed.'.format(name))
    for char in name:
        if char in badChars:
            return __makeErrorDict(name, False,
                                   'The character "{0}" is not allowed.'
                                   .format(char))
    return __makeErrorDict(name, True, None)


def validateVersion(version):
    """Validate the package version.

    @param {String} version The package version.
    @returns {Dictionary} See signature for private __makeErrorDict method.
    """
    version = version.strip()
    # Empty version
    if version == "":
        return __makeErrorDict(version, False, "The version cannot be empty.")

    # Basic semver format
    matches = re.match(r"^(?:\d+[.]){2}\d+$", version)
    if not matches:
        return __makeErrorDict(version, False,
                               'Invalid version: "{0}"'.format(version))
    return __makeErrorDict(version, True, None)


def hasPackageJson(files):
    """Check if package.json is present in the package archive.

    @param {Tuple|List} files Files in the archive.
    @returns {Boolean} True if package.json in list, False otherwise.
    """
    return "package.json" in files


def __isMissingKeys(keys):
    result = False
    allKeys = ("name", "version", "author", "description", "homepage")

    # Check for key existance
    for key in allKeys:
        # There is a missing key in the JSON
        if key not in keys:
            # One of the required keys is missing, abort
            if key in ("name", "version"):
                logging.error("Fatal: missing package.json key: {0}".format(
                              key))
                print(colored.red(
                      "Fatal error: {0} key missing".format(key), bold=True))
                result = True
                break

            # An optional key is missing, issue a warning
            else:
                logging.warning("Missing package.json key: {0}".format(key))
                print(colored.yellow(
                      "Warning: {0} key missing".format(key), bold=True))
    return result


def packageJson(path):
    """Validate the package.json file.

    Validation is defined as containing and filing the required
    keys (name and version), as well as confirming the keys are well-formed.

    A warning is issued for missing or empty optional keys
    but no action is taken and validation result is not affected.

    @param {String} path An absolute path to the package.json file.
    @returns {Boolean} True if all validation tests pass, False otherwise,
    """
    # Read the JSON
    packageJson = jsonutils.read(path)

    # The JSON could not be parsed (most likely invalid)
    if not packageJson:
        logging.error("Unable to read package.json!")
        print(colored.red("Unable to read package.json!", bold=True))
        return False

    # Required key(s) is/are missing
    if __isMissingKeys(tuple(packageJson.keys())):
        return False

    availableValidators = {
        "name": validateName,
        "version": validateVersion
    }

    # Validate each key
    results = []
    for k, v in packageJson.items():
        # Ensure we have a validator for that key
        if k in availableValidators:
            r = availableValidators[k](v)

            # A test failed, collect the error message
            if not r["result"]:
                logging.warning("Validation for key {0} failed!".format(k))
                results.append(r["message"])

    return (results if results else False)
