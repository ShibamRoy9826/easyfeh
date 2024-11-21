## Modules
from os import listdir, walk, getenv,remove
from random import choice
from subprocess import run
from rich.console import Console
from .conf import *
from .webscraper import Downloader


c=Console()

## Config related Functions ##========================================================================================

def write_defaults():
    with open(config_path, "w") as f:
        f.write(default_config)

def setConf(conf):
    with open(config_path, "w") as f:
        dump(conf, f)

def getConf(section,var):
    with open(config_path,"r") as f:
        config=load(f)
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
        c.print("[red underline]Warning[/red underline]: Check your configuration plz, either disable command_on_change or set a valid command!")

## Wallpaper related functions ##========================================================================================

def chooseRandom(directory,more=[]):
    allItems = []
    if path.exists(directory):
        for dirpath, _, filenames in walk(directory):
            for filename in filenames:
                if filename.endswith(tuple(supported_formats)):
                    allItems.append(path.join(dirpath, filename))
    for i in more:
        if path.exists(i):
            for dirpath, _, filenames in walk(i):
                for filename in filenames:
                    if filename.endswith(tuple(supported_formats)):
                        allItems.append(path.join(dirpath, filename))

    if allItems!=[]:
        return choice(allItems)
    else:
        return None

def setRandom(config,use_internet=False,use_down=False):
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
    elif use_down:
        if config["internet"]["use_saved"]:
            moreDirs=[config["internet"]["wallpaper_save_directory"]]
        else:
            moreDirs=[]

        randomWall=chooseRandom("",more=moreDirs)
        if randomWall==None:
            print("Found no proper images, fetching from the internet...")
            setRandom(config,use_internet=True)
        else:
            setWall(randomWall)
            config["internal"]["wall_index"]=-1
            setConf(config)

    else:
        if config["internet"]["use_saved"]:
            moreDirs=[config["internet"]["wallpaper_save_directory"]]
        else:
            moreDirs=[]

        randomWall=chooseRandom(config["wallpaper"]["wallpaper_directory"],more=moreDirs)
        if randomWall==None:
            print("Found no proper images, fetching from the internet...")
            setRandom(config,use_internet=True)
        else:
            setWall(randomWall)
            config["internal"]["wall_index"]=-1
            setConf(config)

def setWall(p, save=True):
    p = path.abspath(p)


    if getConf("other","enabled"):
        cmd = getConf("other","cmd").replace(":f:",p)
        run(f'{cmd}', shell=True,capture_output=False)
    else:
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
    global c
    try:
        with open(history_path, "r") as f:
            print(f.read())
            f.seek(0)
            l=len(f.readlines())
            c.print("[blue]Total wallpapers in history: [/blue]",l)
    except:
        c.print("[red]Error:[/red] Wasn't able to fetch history, are you sure history is turned on in the config file?")

def listInstalled():
    try:
        saveDir=getConf("internet","wallpaper_save_directory")
        count=0
        for i in listdir(saveDir):
            print(path.join(saveDir,i))
            count+=1
        c.print("\n[blue]Total downloaded wallpapers: [/blue]",count)
    except:
        c.print("[red]Error:[/red] Wasn't able to fetch the wallpapers... are you sure that the directory is configured properly in the config file?")

def helpText():
    global c
    c.print(helpTxt)

def showCurrent():
    try:
        with open(history_path,"r") as f:
            curr=f.readlines()[int(getConf("internal","wall_index"))]
            print(curr)
    except:
        c.print("[red]Error:[/red] Wallpaper not found, are you sure that wallpaper history is turned on?")
