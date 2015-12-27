# -*- coding: utf-8 -*-
"""pire - LEGO Racers mods package manager.

Created 2015 Caleb Ely
<http://codetriangle.me/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import re


def validateName(name):
    """Validate the package name.

    @param {String} name The package name.
    @returns {Tuple.<boolean, ?string>} Index 0 will be True if valid name.
                                        If False, index 1 will reason
                                        the name is invalid.
    """
    name = name.strip()
    # Empty package name (default will be used)
    if name == "":
        return (True,)

    # Leading dot/underscore check
    if name[0] == ".":
        return (False, "Sorry, name cannot start with a period.")
    if name[0] == "_":
        return (False, "Sorry, name cannot start with an underscore.")

    # Length check
    if len(name) > 214:
        return (False, "Sorry, name cannot contain more than 214 characters.")

    # Uppercase letter check
    if re.findall(r"[A-Z]", name):
        return (False, "Sorry, name cannot contain capital letters.")

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
    # Empty package version (default will be used)
    if version == "":
        return (True,)

    # Basic semver format
    matches = re.match(r"^(?:[0-9][.]){2}[0-9]$", version)
    if not matches:
        return (False, "Invalid version: \"{0}\"".format(version))
    return (True,)
