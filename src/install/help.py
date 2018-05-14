# -*- coding: utf-8 -*


import src.constants as const


def main():
    message = f"""USAGE
{const.APP_NAME} install <package>

DESCRIPTION
This command installs the specified package into your game.
Place packages in the same directory as {const.APP_NAME} for discovery."""
    print(message)
