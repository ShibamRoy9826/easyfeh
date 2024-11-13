## Modules
from os import listdir, walk, getenv,remove
from random import choice
from subprocess import run
import toml
from conf import *
from webscraper import Downloader

## Config related Functions ##========================================================================================


def write_defaults():
    with open(config_path, "w") as f:
        f.write(default_config)

def setConf(conf):
    with open(config_path, "w") as f:
        toml.dump(conf, f)

def getConf(section,var):
    with open(config_path,"r") as f:
        config=toml.load(f)
    return config[section][var]

def returnSource():
    if getConf("internet","image_source")=="unsplash":
        return 0
    else:
        return 1

def resetHistory(index,nothing=False):
    if nothing:
        with open(history_path, "w") as fl:
            fl.write('')
    else:
        with open(history_path, "r") as f:
            last = f.readlines()[index]
        with open(history_path, "w") as fl:
            fl.write(last)

def resetDownloaded():
    with open(history_path, "r") as f:
        hist=f.readlines()
        lastUsed=hist[int(getConf("internal","wall_index"))]

    toRemove=[]
    for img in listdir(getConf("internet","wallpaper_save_directory")):
        if img in lastUsed:
            pass
        else:
            toRemove.append(path.join(getConf("internet","wallpaper_save_directory"),img))
    for i in toRemove:
        remove(i)


def appendHistory(p):
    try:
        with open(history_path, "r") as fl:
            a = fl.readlines()
            last = a[-1]
            if len(a) >= int(getConf("wallpaper","wallpaper_history_limit")):
                resetHistory(int(getConf("internal","wall_index")),nothing=True)
    except Exception as e:
        print(e)
        last = ""
    with open(history_path, "a") as f:
        if p + "\n" != last:
            f.write(p + "\n")


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


def chooseRandom(directory,more=[]):

    allItems = []
    if path.exists(directory):
        for dirpath, _, filenames in walk(directory):
            for filename in filenames:
                allItems.append(path.join(dirpath, filename))
    for i in more:
        if path.exists(i):
            for dirpath, _, filenames in walk(i):
                for filename in filenames:
                    allItems.append(path.join(dirpath, filename))
    if allItems!=[]:
        return choice(allItems)
    else:
        return None

def setRandom(config,use_internet=False):
    if use_internet:
        q=getConf("internet","image_query")
        if q=="":
            src=returnSource()
            d=Downloader("landscape",source=returnSource())
            d.download(count=1)
            setWall(d.images[0])
        else:
            d=Downloader(q,source=returnSource())
            d.download(count=1)
            setWall(d.images[0])
    else:
        if config["internet"]["use_saved"]:
            moreDirs=[config["internet"]["wallpaper_save_directory"]]
        else:
            moreDirs=[]

        randomWall=chooseRandom(config["wallpaper"]["wallpaper_directory"],more=moreDirs)
        if randomWall==None:
            setRandom(config,use_internet=True)
        else:
            setWall(randomWall)
            config["internal"]["wall_index"]=-1
            setConf(config)


def setWall(p, save=True):
    p = path.abspath(p)
    if getenv("XDG_SESSION_TYPE")=="x11":
        options = getConf("feh","options") 
        run(f"feh {options} {p}", shell=True, capture_output=False)
    else:
        options = getConf("swww","options")
        run(f"swww img {p} {options}",shell=True,capture_output=False)

    if save and getConf("wallpaper","remember_wallpaper"):
        appendHistory(p)
    print("Done! Wallpaper has been set:)")


## Printing functions ##========================================================================================


def printHistory():
    with open(history_path, "r") as f:
        print(f.read())


def helpText():
    print(helpTxt)
