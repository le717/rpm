# -*- coding: utf-8 -*


import src.constants as const


def main():
    message = """Usage: {0} install <package>

DESCRIPTION
This command installs the specified package into your game.""".format(
        const.APP_NAME)
    print(message)
