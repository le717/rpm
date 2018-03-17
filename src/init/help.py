# -*- coding: utf-8 -*


import src.constants as const


def main():
    message = f"""Usage: {const.APP_NAME} init

DESCRIPTION
This command creates the boilerplate structure for a new package.
When successfully run, the following items are created in the directory
{const.APP_NAME} was run from.

| GAMEDATA/
| MENUDATA/
| package.json

When creating your package, you should put the relevant files inside each
folder. You are required to create all necessary subfolders needed.

package.json contains the package details you supply when the command is run.
If you need to edit the details, you can open it in your preferred text editor.
For details on the JSON format and how to edit it, Copter Labs has written
an excellent article on the subject.
https://www.copterlabs.com/json-what-it-is-how-it-works-how-to-use-it/"""
    print(message)
