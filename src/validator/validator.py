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

__all__ = ("PACKAGE_NAME_MAX_LENGTH", "validateName", "validateVersion",
           "isMissingKeys", "hasPackageJson", "packageJson")


PACKAGE_NAME_MAX_LENGTH = 214


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
        return __makeErrorDict(name, "error", "name cannot be empty.")

    # Leading dot/underscore check
    if name[0] == ".":
        return __makeErrorDict(name, "error",
                               "name cannot start with a period.")
    if name[0] == "_":
        return __makeErrorDict(name, "error",
                               "name cannot start with an underscore.")

    # Spaces check
    if re.findall(r"\s", name):
        return __makeErrorDict(name, "error", "name cannot contain spaces.")

    # Length check
    if len(name) > PACKAGE_NAME_MAX_LENGTH:
        return __makeErrorDict(name, "error",
                               "name cannot contain more than"
                               " {0} characters.".format(
                                   PACKAGE_NAME_MAX_LENGTH))

    # Uppercase letter check
    if re.findall(r"[A-Z]", name):
        return __makeErrorDict(name, "error",
                               "name cannot contain capital letters.")

    badChars = ("\\", "/", ":", "*", "?", '"', "<", ">", "|")
    badNames = ("aux", "com1", "com2", "com3", "com4", "con",
                "lpt1", "lpt2", "lpt3", "prn", "nul")

    # Invalid Windows names/charcters check
    if name in badNames:
        return __makeErrorDict(name, "error",
                               'name "{0}" is not allowed.'.format(name))
    for char in name:
        if char in badChars:
            return __makeErrorDict(name, "error",
                                   'character "{0}" is not allowed.'
                                   .format(char))
    return __makeErrorDict(name, None, None)


def validateVersion(version):
    """Validate the package version.

    @param {String} version The package version.
    @returns {Dictionary} See signature for private __makeErrorDict method.
    """
    version = version.strip()
    # Empty version
    if version == "":
        return __makeErrorDict(version, "error", "version cannot be empty.")

    # Basic semver format
    matches = re.match(r"^(?:\d+[.]){2}\d+$", version)
    if not matches:
        return __makeErrorDict(version, "error",
                               'Invalid version: "{0}"'.format(version))
    return __makeErrorDict(version, None, None)


def hasPackageJson(files):
    """Check if package.json is present in the package archive.

    @param {Tuple|List} files Files in the archive.
    @returns {Boolean} True if package.json in list, False otherwise.
    """
    return "package.json" in files


def isMissingKeys(keys):
    results = []
    allKeys = ("name", "version", "author", "description", "homepage")

    # Check for key existance
    for key in allKeys:
        if key not in keys:
            msg = 'missing key "{0}"'.format(key)

            # A required key is missing
            if key in ("name", "version"):
                results.append(__makeErrorDict(key, "error", msg))
                logging.error(msg)

            # An optional key is missing
            else:
                results.append(__makeErrorDict(key, "warning", msg))
                logging.warning(msg)
    return (results if results else False)


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
    results = []
    logging.info("Validating package.json")
    packageJson = jsonutils.read(path)

    # The JSON could not be parsed (most likely invalid)
    # TODO Move this check to hasPackageJson()
    if not packageJson:
        logging.error("Unable to read package.json!")
        results.append(__makeErrorDict(None, "warning",
                       "Unable to read package.json!"))
        return results

    # Required key(s) is/are missing
    missing = isMissingKeys(tuple(packageJson.keys()))
    if missing:
        results = [_ for _ in missing]

    availableValidators = {
        "name": validateName,
        "version": validateVersion
    }

    # Validate each key
    for k, v in packageJson.items():
        # Ensure we have a validator for that key
        if k in availableValidators:
            valid = availableValidators[k](v)

            # A test failed
            if valid["result"]:
                logging.warning("Validation for key {0} failed!".format(k))
                results.append(valid)

    return (results if results else False)
