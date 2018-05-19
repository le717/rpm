# -*- coding: utf-8 -*

import src.constants as const


def main():
    message = f"""USAGE
{const.APP_NAME} package <directory>

DESCRIPTION
This command creates a completed package for distribution.
Packages details will be read from the package.json file in the directory
and used when saving the package.

This command could take a few minutes to run, depending on the
amount of files the package contains.

Extensive file filtering is not performed while creating a package.
It is your responsibility to ensure all files in the directory should be
included in the final package.
"""
    print(message)
