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


def validateName(name):
    """Validate the package name.

    @param {String} name The package name.
    @returns {Tuple.<boolean, ?string>} Index 0 will be True if valid name.
                                        If False, index 1 will reason
                                        the name is invalid.
    """
    name = name.strip()
    # Empty name
    if name == "":
        return (False, "The name cannot be empty.")

    # Leading dot/underscore check
    if name[0] == ".":
        return (False, "The name cannot start with a period.")
    if name[0] == "_":
        return (False, "The name cannot start with an underscore.")

    # Spaces check
    if re.findall(r"\s", name):
        return (False, "The name cannot contain spaces.")

    # Length check
    if len(name) > 214:
        return (False, "The name cannot contain more than 214 characters.")

    # Uppercase letter check
    if re.findall(r"[A-Z]", name):
        return (False, "The name cannot contain capital letters.")

    badChars = ("\\", "/", ":", "*", "?", '"', "<", ">", "|")
    badNames = ("aux", "com1", "com2", "com3", "com4", "con",
                "lpt1", "lpt2", "lpt3", "prn", "nul")

    # Invalid Windows names/charcters check
    if name in badNames:
        return (False, "Name \"{0}\" is not allowed.".format(name))
    for char in name:
        if char in badChars:
            return (False, "The character \"{0}\" is not allowed.".format(
                    char))
    return (True,)


def validateVersion(version):
    """Validate the package version.

    @param {String} version The package version.
    @returns {Tuple.<boolean, ?string>} Index 0 will be True if valid version.
                                        If False index 1 will be error message.
    """
    version = version.strip()
    # Empty version
    if version == "":
        return (False, "The version cannot be empty.")

    # Basic semver format
    matches = re.match(r"^(?:[0-9][.]){2}[0-9]$", version)
    if not matches:
        return (False, "Invalid version: \"{0}\"".format(version))
    return (True,)


def hasPackageJson(files):
    """Check if package.json is present in the package archive.

    @param {Tuple|List} files Files in the archive.
    @returns {Boolean} True if package.json in list, False otherwise.
    """
    return "package.json" in files


def __isMissingKey(keys):
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
    if __isMissingKey(tuple(packageJson.keys())):
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
            if not r[0]:
                logging.warning("Validation for key {0} failed!".format(k))
                results.append(r[1])

    return (results if results else False)
