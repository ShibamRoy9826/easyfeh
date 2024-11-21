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
                c.print("[red]File not found[/red], ",end="")
                if getConf("internet","use_from_internet"):
                    print("fetching from internet")
                    setRandom(config,use_internet=True)
                else:
                    print("setting a random one")
                    setRandom(config)

            ran=True

        if ("-reset-hist" in options) or ("-rh" in options):
            confirm=c.input("[yellow]Are you sure you want to clear your history? (y/n) :[/yellow]")
            if confirm.lower()=="y":
                resetHistory(getConf("internal", "wall_index"))
                print("Done!")
            else:
                print("Aborted...")
            ran=True
        if ("-reset-conf" in options) or ("-rc" in options):
            confirm=c.input("[yellow]Are you sure you want to reset your configuration? (y/n) :[/yellow]")
            if confirm.lower()=="y":
                write_defaults()
                print("Done!")
            else:
                print("Aborted...")
            ran=True
        if ("-reset-walls" in options) or ("-rw" in options):
            confirm=input("[yellow]Are you sure you want to all wallpapers delete? (y/n) :[/yellow]")
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
                        c.print("[red]Previous wallpaper doesn't exist anymore...[/red]")
            except:
                c.print(
                        "[red]Error: No previous wallpaper found. [/red](Maybe already on oldest, Check history!)"
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
                            print("[red]Next wallpaper doesn't exist anymore...[/red]")
                    else:
                        print(
                                "[red]Error: No next wallpaper found. [/red](Maybe already on latest, Check history!)"
                        )
            except:
                print(
                        "[red]Error: No next wallpaper found. [/red](Maybe already on latest, Check history!)"
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
            amount=1
            source="wallhaven"
            query=getConf("internet","image_query")
            for ind,i in enumerate(argv):
                if i=="-download" or i=="-d":
                    try:
                        amount=int(argv[ind+1])
                    except (IndexError,ValueError):
                        c.print("[yellow]Warning: You didn't specify a valid number of images[/yellow], using default(1)") 
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
            c.print(f"Searching for [green]{query}[/green] in [green]{source}[/green]")
            d=Downloader(query,source=returnSourceParam(source))
            d.download(count=amount)
            c.print(f"[green]Successfully downloaded [yellow]{amount}[/yellow] wallpaper(s)![/green]")



        if "-h" in options or "-help" in options:
            helpText()
            ran=True
        if ran==False:
            c.print("[red]No such command found:( [/red] , try running [green]'easyfeh -h'[/green]")
            
            
if __name__=="__main__":
    main()
