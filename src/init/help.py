# -*- coding: utf-8 -*


import src.constants as const


def main():
    message = """Usage: {0} init

DESCRIPTION
This command creates a boilerplate folder structure for a new package.""".format(
        const.APP_NAME)
    print(message)
