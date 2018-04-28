# -*- coding: utf-8 -*-
"""rpm - LEGO Racers mods package manager.

Created 2015-2018 Caleb Ely
<https://CodeTri.net/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import re
import logging
from src.utils import jsonutils

__all__ = ("PACKAGE_NAME_MAX_LENGTH", "validate_name", "validate_version",
           "is_missing_keys", "has_package_json", "package_json")


PACKAGE_NAME_MAX_LENGTH = 214


def __make_error_dict(value, result, message):
    """Create an error dictionary.

    @param {*} value The value in question that caused the error.
    @param {*} result The error status.
    @param {*} message The error message.
    @return {Dictionary.<value, result, message>} An error dictionary.
                                                  Keys are same as params.
    """
    return {
        "message": message,
        "result": result,
        "value": value
    }


def validate_name(name):
    """Validate the package name.

    @param {String} name The package name.
    @return {Dictionary} See signature for private __make_error_dict method.
    """
    name = name.strip()
    # Empty name
    if name == "":
        return __make_error_dict(name, "error", "name cannot be empty.")

    # Leading dot/underscore check
    if name[0] == ".":
        return __make_error_dict(
            name,
            "error",
            "name cannot start with a period."
        )

    if name[0] == "_":
        return __make_error_dict(
            name,
            "error",
            "name cannot start with an underscore."
        )

    # Spaces check
    if re.findall(r"\s", name):
        return __make_error_dict(name, "error", "name cannot contain spaces.")

    # Length check
    if len(name) > PACKAGE_NAME_MAX_LENGTH:
        return __make_error_dict(
            name,
            "error",
            "name cannot contain more than"
            f" {PACKAGE_NAME_MAX_LENGTH} characters."
        )

    # Uppercase letter check
    if re.findall(r"[A-Z]", name):
        return __make_error_dict(
            name,
            "error",
            "name cannot contain capital letters."
        )

    badChars = ("\\", "/", ":", "*", "?", '"', "<", ">", "|")
    badNames = ("aux", "com1", "com2", "com3", "com4", "con",
                "lpt1", "lpt2", "lpt3", "prn", "nul")

    # Invalid Windows names/charcters check
    if name in badNames:
        return __make_error_dict(
            name,
            "error",
            f'name "{name}" is not allowed.'
        )

    for char in name:
        if char in badChars:
            return __make_error_dict(
                name,
                "error",
                f'character "{char}" is not allowed.'
            )
    return __make_error_dict(name, None, None)


def validate_version(version):
    """Validate the package version.

    @param {String} version The package version.
    @return {Dictionary} See signature for private __make_error_dict method.
    """
    version = version.strip()
    # Empty version
    if version == "":
        return __make_error_dict(version, "error", "version cannot be empty.")

    # Basic semver format
    matches = re.match(r"^(?:\d+[.]){2}\d+$", version)
    if not matches:
        return __make_error_dict(
            version,
            "error",
            f'Invalid version: "{version}"'
        )
    return __make_error_dict(version, None, None)


def has_package_json(files):
    """Check if package.json is present in the package archive.

    @param {Tuple|List} files Files in the archive.
    @return {Boolean} True if package.json in list, False otherwise.
    """
    return "package.json" in files


def is_missing_keys(keys):
    results = []
    all_keys = ("name", "version", "author", "description", "homepage")

    # Check for key existance
    for key in all_keys:
        if key not in keys:
            msg = f'missing key "{key}"'

            # A required key is missing
            if key in ("name", "version"):
                results.append(__make_error_dict(key, "error", msg))
                logging.error(msg)

            # An optional key is missing
            else:
                results.append(__make_error_dict(key, "warning", msg))
                logging.warning(msg)
    return results if results else False


def package_json(path):
    """Validate the package.json file.

    Validation is defined as containing and filing the required
    keys (name and version), as well as confirming the keys are well-formed.

    A warning is issued for missing or empty optional keys
    but no action is taken and validation result is not affected.

    @param {String} path An absolute path to the package.json file.
    @return {Boolean} True if all validation tests pass, False otherwise,
    """
    # Read the JSON
    results = []
    logging.info("Validating package.json")
    package_json = jsonutils.read(path)

    # The JSON could not be parsed (most likely invalid)
    if not package_json:
        logging.error("Unable to read package.json!")
        results.append(__make_error_dict(None, "error",
                       "Unable to read package.json!"))
        return results

    # Required key(s) is/are missing
    missing = is_missing_keys(tuple(package_json.keys()))
    if missing:
        results = missing

    available_validators = {
        "name": validate_name,
        "version": validate_version
    }

    # Validate each key
    for k, v in package_json.items():
        # Ensure we have a validator for that key
        if k in available_validators:
            valid = available_validators[k](v)

            # A test failed
            if valid["result"]:
                logging.warning(f"Validation for key {k} failed!")
                results.append(valid)

    return results if results else False
