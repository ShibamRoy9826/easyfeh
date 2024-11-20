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
# import traceback # Occasionally for debugging
from sys import argv
from .conf import *
from .functions import *

def main():
## Loading Configuration ##========================================================================
    with open(config_path, "r") as f:
        config = load(f)

## Main Program ##======================================================================

    options = []
    img_path = ""

    for ind, i in enumerate(argv):
        if ind != 0:
            if i.startswith("-"):
                options.append(i)
            else:
                img_path = i
    ran=False

# If nothing is given
    if len(options) == 0 and img_path == "":
        helpText()
        ran=True
    elif len(options) == 0:
        setWall(img_path)
        ran=True
    else:
        if ("-restore" in options) or ("-res" in options):
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
                print("File not found, ",end="")
                if getConf("internet","use_from_internet"):
                    print("fetching from internet")
                    setRandom(config,use_internet=True)
                else:
                    print("setting a random one")
                    setRandom(config)

            ran=True

        if ("-reset-hist" in options) or ("-rh" in options):
            confirm=input("Are you sure you want to clear your history? (y/n) :")
            if confirm.lower()=="y":
                resetHistory(getConf("internal", "wall_index"))
                print("Done!")
            else:
                print("Aborted...")
            ran=True
        if ("-reset-conf" in options) or ("-rc" in options):
            confirm=input("Are you sure you want to reset your configuration? (y/n) :")
            if confirm.lower()=="y":
                write_defaults()
                print("Done!")
            else:
                print("Aborted...")
            ran=True
        if ("-reset-walls" in options) or ("-rw" in options):
            confirm=input("Are you sure you want to all wallpapers delete? (y/n) :")
            if confirm.lower()=="y":
                resetDownloaded()
                print("Done!")
            else:
                print("Aborted...")
            ran=True
        if ("-prev" in options) or ("-p" in options):
            try:
                with open(history_path, "r") as f:
                    walls = f.readlines()
                    newIndex = int(config["internal"]["wall_index"]) - 1
                    toSet = walls[newIndex].replace("\n","")
                    if path.isfile(toSet):
                        setWall(toSet, save=False)
                        config["internal"]["wall_index"] = newIndex
                        setConf(config)
                    else:
                        print("Previous wallpaper doesn't exist anymore...")
            except:
                print(
                    "No previous wallpaper found. (Maybe already on oldest, Check history!)"
                )
            ran=True
        if ("-next" in options) or ("-n" in options):
            try:
                with open(history_path, "r") as f:
                    walls = f.readlines()
                    newIndex = int(config["internal"]["wall_index"]) + 1
                    if newIndex != 0:
                        config["internal"]["wall_index"] = newIndex
                        setConf(config)
                        toSet = walls[newIndex].replace("\n","")
                        if path.isfile(toSet):
                            setWall(toSet, save=False)
                        else:
                            print("Next wallpaper doesn't exist anymore...")
                    else:
                        print(
                            "No next wallpaper found. (Maybe already on latest, Check history!)"
                        )
            except:
                print(
                    "No next wallpaper found. (Maybe already on latest, Check history!)"
                )
            ran=True
        elif (("-random" in options) and ("-use-internet" in options)) or (("-r" in options) and ("-ui" in options)):
            setRandom(config, use_internet=True)
            ran=True
        elif ("-random" in options) and ("-use-down" in options) or (("-r" in options) and ("-ud" in options)) :
            setRandom(config,use_down=True)
            ran=True
        elif ("-random" in options) or ("-r" in options):
            if getConf("internet","use_from_internet"):
                setRandom(config,use_internet=True)
            else:
                setRandom(config)
            ran=True
        if ("-show-hist" in options) or ("-sh" in options):
            printHistory()
            ran=True

        if ("-show-down" in options) or ("-sd" in options):
            listInstalled()
            ran=True
        
        if ("-show-curr" in options) or ("-sc" in options):
            showCurrent()
            ran=True
        if ("-download" in options) or ("-d" in options):
            ran=True
            try:
                amount=1
                source="wallhaven"
                query=getConf("internet","image_query")
                for ind,i in enumerate(argv):
                    if i=="-download" or i=="-d":
                        try:
                            amount=int(argv[ind+1])
                        except (IndexError,ValueError):
                            pass
                    if i=="-query" or i=="-q":
                        try:
                            query=argv[ind+1]
                        except IndexError:
                            pass
                    if i=="-source" or i=="-s":
                        try:
                            source=argv[ind+1]
                        except IndexError:
                            pass
                print(f"Searching for {query} in {source}")
                d=Downloader(query,source=returnSourceParam(source))
                d.download(count=amount)
                print(f"Successfully downloaded {amount} wallpapers!")
            except IndexError:
                print("Error: Please specify the number of pictures to download...") 



        if "-h" in options or "-help" in options:
            helpText()
            ran=True
        if ran==False:
            print("No such command found:(  , try running 'easyfeh -h'")
            
            
if __name__=="__main__":
    main()
