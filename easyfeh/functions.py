## Modules
from os import listdir, walk, getenv,remove
from os.path import isfile
from random import choice
from subprocess import run
import toml
from .conf import *
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
    return int(getConf("internet","image_source").lower()!="unsplash")
def returnSourceParam(param):
    return int(param.lower()!="unsplash")
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
    try:
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
    except (FileNotFoundError,IndexError):
        for img in listdir(getConf("internet","wallpaper_save_directory")):
            remove(path.join(getConf("internet","wallpaper_save_directory"),img))
    

def appendHistory(p):
    if path.isfile(history_path):
        try:
            with open(history_path, "r") as fl:
                a = fl.readlines()
                last = a[-1]
                if len(a) >= int(getConf("wallpaper","wallpaper_history_limit")):
                    resetHistory(int(getConf("internal","wall_index")),nothing=True)
        except IndexError:
            last = ""
        with open(history_path, "a") as f:
            if p + "\n" != last:
                f.write(p + "\n")

## Additional functionalities ##=========================================================================================

def sendNotif(path):
    heading=getConf("triggers","notif_message")
    body=getConf("triggers","notif_body").replace(":f:",path)
    run(f"""notify-send "{heading}" "{body}" """, shell=True, capture_output=False)

def runOnChange():
    cmd=getConf("triggers","command")
    if cmd!="":
        run(cmd,shell=True,capture_output=False)
    else:
        print("Warning: Check your configuration plz, either disable command_on_change or set a valid command!")

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
    if getConf("triggers","notify_on_change"):
        sendNotif(p)
        
    if getConf("triggers","command_on_change"):
        runOnChange()



## Printing functions ##========================================================================================

def printHistory():
    try:
        with open(history_path, "r") as f:
            print(f.read())
            f.seek(0)
            l=len(f.readlines())
            print("Total wallpapers in history: ",l)
    except:
        print("Error: Wasn't able to fetch history, are you sure history is turned on in the config file?")

def listInstalled():
    try:
        for i in listdir(getConf("internet","wallpaper_save_directory")):
            print(i)
    except:
        print("Error: Wasn't able to fetch the wallpapers... are you sure that the directory is configured properly in the config file?")

def helpText():
    print(helpTxt)

def showCurrent():
    try:
        with open(history_path,"r") as f:
            curr=f.readlines()[int(getConf("internal","wall_index"))]
            print(curr)
    except:
        print("Error: Wallpaper not found, are you sure that wallpaper history is turned on?")
