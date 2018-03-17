#! /usr/bin/env python3
"""rpm - LEGO Racers mods package manager.

Created 2015-2018 Caleb Ely
<https://CodeTri.net/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""


import os
from cx_Freeze import (setup, Executable)

from src import constants as const


# Output folder
dest_folder = "bin"

# Create the freeze path if it doesn't exist
if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)

build_exe_options = {
    "build_exe": dest_folder,
    "optimize": 2,
    "bin_path_excludes": [".vscode", "tests"]
}

setup(
    name=const.APP_NAME,
    version=const.VERSION,
    author=const.VERSION,
    description=f"{const.APP_NAME} v{const.VERSION}",
    license="MIT",
    options={"build_exe": build_exe_options},
    executables=[Executable("rpm.py", targetName="rpm.exe")]
)
