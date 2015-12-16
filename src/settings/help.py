# -*- coding: utf-8 -*


import src.constants as const


def main():
    message = """Usage: {0} settings

DESCRIPTION
This command allows you to adjust user-defined settings.""".format(
        const.APP_NAME)
    print(message)
