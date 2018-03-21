# -*- coding: utf-8 -*


import src.constants as const


def main():
    message = f"""USAGE
{const.APP_NAME} settings

DESCRIPTION
This command allows you to adjust user-defined settings.

In order to install packages, you need to tell {const.APP_NAME} where
to find your LEGO Racers installation. Do this by running
`{const.APP_NAME} settings` and entering the path to your game.
Do not point to any specific file, as that is not needed.
Once a valid game installation is confirmed, {const.APP_NAME} will configure
itself to manage packages according to the game revision you own.

If at any time your game installation changes location or needs to be
reconfigured, simply run the command again to restart the process.

If you would like to learn more about the game differences between
revisions, Rock Raiders United is an excellent resource for all things
LEGO video games. http://www.rockraidersunited.com"""
    print(message)
