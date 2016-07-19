# -*- coding: utf-8 -*


import src.constants as const


def main():
    message = """Usage: {0} settings

DESCRIPTION
This command allows you to adjust user-defined settings.

In order to install packages, you need to tell {0} where
to find your LEGO Racers installation. Do this by running `{0} settings`
and entering the path to your game. Do not point to any specific file,
as that is not needed. Once a valid game installation is confirmed,
{0} will configure itself to manage packages according to the
game revision you own.

If at any time your game installation changes location or needs to be
configured, simply run the command again to restart the process.

If you would like to learn more about the game differences between
revisions, Rock Raiders United is an excellent resource for all things
LEGO video games. http://www.rockraidersunited.com""".format(
        const.APP_NAME)
    print(message)
