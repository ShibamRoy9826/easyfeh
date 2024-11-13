"""
███████╗ █████╗ ███████╗██╗   ██╗███████╗███████╗██╗  ██╗
██╔════╝██╔══██╗██╔════╝╚██╗ ██╔╝██╔════╝██╔════╝██║  ██║
█████╗  ███████║███████╗ ╚████╔╝ █████╗  █████╗  ███████║
██╔══╝  ██╔══██║╚════██║  ╚██╔╝  ██╔══╝  ██╔══╝  ██╔══██║
███████╗██║  ██║███████║   ██║   ██║     ███████╗██║  ██║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝ 
By Shibam Roy
"""

## Modules ##=========================================================================================
# import traceback
from os import mkdir
from sys import argv

import toml

from conf import *
from functions import *

## Loading Configuration ##========================================================================
with open(config_path, "r") as f:
    config = toml.load(f)

## Main Program ##======================================================================

options = []
img_path = ""

for ind, i in enumerate(argv):
    if ind != 0:
        if i.startswith("-"):
            options.append(i)
        else:
            img_path = i

# If nothing is given
if len(options) == 0 and img_path == "":
    helpText()
elif len(options) == 0:
    setWall(img_path)
else:
    if "-restore" in options:
        try:
            with open(path.join(config_directory, "history.txt"), "r") as f:
                walls = f.readlines()
                p=walls[config["internal"]["wall_index"]].replace("\n","")
                if not path.isfile(p):
                    raise FileNotFoundError
                else:
                    setWall(p, save=False)
                    print("Set to last used wallpaper!")
        except:
            if getConf("internet","use_from_internet"):
                setRandom(config,use_internet=True)
            else:
                setRandom(config)


    if "-reset-hist" in options:
        resetHistory(getConf("internal", "wall_index"))
    if "-reset-conf" in options:
        write_defaults()
    if "-reset-walls" in options:
        resetDownloaded()
    if "-prev" in options:
        try:
            with open(history_path, "r") as f:
                walls = f.readlines()
                newIndex = int(config["internal"]["wall_index"]) - 1
                config["internal"]["wall_index"] = newIndex
                setConf(config)
                toSet = walls[newIndex]
                setWall(toSet, save=False)
        except:
            print(
                "No previous wallpaper found. (Maybe already on oldest, Check history!)"
            )
    if "-next" in options:
        try:
            with open(history_path, "r") as f:
                walls = f.readlines()
                newIndex = int(config["internal"]["wall_index"]) + 1
                if newIndex != 0:
                    config["internal"]["wall_index"] = newIndex
                    setConf(config)
                    toSet = walls[newIndex]
                    setWall(toSet, save=False)
                else:
                    print(
                        "No next wallpaper found. (Maybe already on latest, Check history!)"
                    )
        except:
            print(
                "No next wallpaper found. (Maybe already on latest, Check history!)"
            )
    elif ("-random" in options) and ("-use-internet" in options):
        setRandom(config, use_internet=True)
    elif "-random" in options:
        if getConf("internet","use_from_internet"):
            setRandom(config,use_internet=True)
        else:
            setRandom(config)

    if "-show-hist" in options:
        printHistory()

    if "-h" in options or "-help" in options:
        helpText()
