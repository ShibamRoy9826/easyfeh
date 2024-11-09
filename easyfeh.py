"""
███████╗ █████╗ ███████╗██╗   ██╗███████╗███████╗██╗  ██╗
██╔════╝██╔══██╗██╔════╝╚██╗ ██╔╝██╔════╝██╔════╝██║  ██║
█████╗  ███████║███████╗ ╚████╔╝ █████╗  █████╗  ███████║
██╔══╝  ██╔══██║╚════██║  ╚██╔╝  ██╔══╝  ██╔══╝  ██╔══██║
███████╗██║  ██║███████║   ██║   ██║     ███████╗██║  ██║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝ 
By Shibam Roy
"""

from os import mkdir
from sys import argv

import toml

from conf import *
import traceback
## Modules ##=========================================================================================
from functions import *

## Create Config if it doesn't exist ##==============================================================

if "easyfeh" not in listdir(config_directory):
    mkdir(config_directory + "/easyfeh")
else:
    if not path.isfile(config_path):
        write_defaults()
    if not path.isfile(path.join(config_directory, "history.txt")):
        with open(path.join(config_directory, "history.txt"), "w") as f:
            pass


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
        with open(path.join(config_directory,"history.txt"),'r') as f:
            walls=f.readlines()
            setWall(walls[config["internal"]["wall_index"]],save=False)
            print("Set to last used wallpaper!")
        
    if "-reset-hist" in options:
        resetHistory()
    if "-reset-conf" in options:
        write_defaults()
    if "-prev" in options:
        with open(history_path, "r") as f:
            walls = f.readlines()
            try:
                newIndex=int(config["internal"]["wall_index"]) - 1
                config["internal"]["wall_index"]=newIndex
                setConf(config)
                toSet = walls[newIndex]
                setWall(toSet,save=False)
            except:
                print(
                    "No previous wallpaper found. (Maybe already on oldest, Check history!)"
                )
    if "-next" in options:
        with open(history_path, "r") as f:
            walls = f.readlines()
            try:
                newIndex=int(config["internal"]["wall_index"]) + 1
                if newIndex!=0:
                    config["internal"]["wall_index"]=newIndex
                    setConf(config)
                    toSet = walls[newIndex]
                    setWall(toSet,save=False)
                else:
                    print(
                        "No next wallpaper found. (Maybe already on latest, Check history!)"
                    )
            except:
                print(
                    "No next wallpaper found. (Maybe already on latest, Check history!)"
                )
    if "-random" in options:
        setRandom(config)

    if "-show-hist" in options:
        printHistory()

    if "-h" in options or "-help" in options:
        helpText()
