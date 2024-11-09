## Modules
from os import listdir, walk, getenv
from random import choice
from subprocess import run

import toml

from conf import *

## Config related Functions ##========================================================================================


def write_defaults():
    with open(config_path, "w") as f:
        f.write(default_config)


def resetHistory():
    with open(history_path, "r") as f:
        last = f.readlines()[-1]
    with open(history_path, "w") as fl:
        fl.write(last)


def appendHistory(p):
    try:
        with open(history_path, "r") as fl:
            a = fl.readlines()
            last = a[-1]
            if len(a) >= 50:
                resetHistory()
    except:
        last = ""
    with open(history_path, "a") as f:
        if p + "\n" != last:
            f.write(p + "\n")


def setConf(conf):
    with open(config_path, "w") as f:
        toml.dump(conf, f)

def getConf(section,var):
    with open(config_path,"r") as f:
        config=toml.load(f)
    return config[section][var]


## Wallpaper related functions ##========================================================================================


def filterWall(p):
    try:
        allItems = listdir(p)
    except:
        allItems = []
        print("Wallpaper folder doesn't exist!")
    supportedFormats = ["jpg", "jpeg", "png", "pnm", "tiff", "bmp", "gif"]
    if len(allItems) == 0:
        return []
    else:
        filtered = []
        for i in allItems:
            if i.rsplit(".", 1)[1] in supportedFormats:
                filtered.append(path.join(p, i))
        return filtered


def chooseRandom(directory):
    allItems = []
    for dirpath, _, filenames in walk(directory):
        for filename in filenames:
            allItems.append(path.join(dirpath, filename))
    return choice(allItems)


def setRandom(config):
    setWall(chooseRandom(config["wallpaper"]["wallpaper_directory"]))


def setWall(p, save=True):
    p = path.abspath(p)
    if getenv("XDG_SESSION_TYPE")=="x11":
        options = getConf("feh","options") 
        run(f"feh {options} {p}", shell=True, capture_output=False)
    else:
        options = getConf("swww","options")
        run(f"swww img {p} {options}",shell=True,capture_output=False)

    if save:
        appendHistory(p)
    print("Done! Wallpaper has been set:)")


## Printing functions ##========================================================================================


def printHistory():
    with open(history_path, "r") as f:
        print(f.read())


def helpText():
    print(helpTxt)
