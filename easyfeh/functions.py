## Modules
from os import getenv, listdir, remove, walk
from random import choice
from subprocess import run

from rich.console import Console

from .conf import *
from .webscraper import Downloader

c = Console()

def showErr(msg):
    c.print(f"[red bold]Error:[/red bold] {msg}")
## Config related Functions ##========================================================================================


def write_defaults() -> None:
    with open(config_path, "w") as f:
        f.write(default_config)


def rgbToHex(rgb: Union[list, tuple]) -> str:
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]

    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def isLight(r: Union[int, float], g: Union[int, float], b: Union[int, float]) -> bool:
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    threshold = 0.5
    return luminance > threshold

def writePalette(palette: Union[list, tuple], fl_path="", general=False) -> None:
    if general:
        fl_path = getConf("palette", "complete_palette_path")
        primary = rgbToHex(palette[1])
        secondary = rgbToHex(palette[3])
        bg = rgbToHex(palette[0])
        if isLight(palette[0][0], palette[0][1], palette[0][2]):
            fg = "#11111b"
            fg2 = "#313244"
        else:
            fg = "#cdd6f4"
            fg2 = "#9399b2"
        urgent = "#f38ba8"

        content = f"""bg: {bg};
fg: {fg};
fg2: {fg2};
primary: {primary};
secondary: {secondary};
urgent: {urgent};
        """
        with open(fl_path, "w") as f:
            f.write(content)

    else:

        if fl_path == "":
            fl_path = getConf("palette", "palette_path")
        plt = ""
        for i in palette:
            plt += f"{str(i[0])} {str(i[1])} {(i[2])}        {rgbToHex(i)}\n"

        with open(fl_path, "w") as f:
            f.write(plt)


def setConf(conf) -> None:
    with open(config_path, "w") as f:
        dump(conf, f)


def getConf(section, var):
    try:
        with open(config_path, "r") as f:
            config = load(f)
        return config[section][var]
    except (KeyError,FileNotFoundError):
        showErr(f"Unable to find {var}, in {section} section of the configuration")
        return None

def returnSource() -> int:
    try:
        s=getConf("internet", "image_source").lower()
        if s=="unsplash":
            return 0
        else:
            return 1

    except AttributeError:
        return 1

def returnSourceParam(param: str) -> int:
    return int(param.lower() != "unsplash")


def resetHistory(index: int, nothing=False) -> None:

    if nothing:
        with open(history_path, "w") as fl:
            fl.write("")
    else:
        try:
            with open(history_path, "r") as f:
                last = f.readlines()[index]

            with open(history_path, "w") as fl:
                fl.write(last)

        except (FileNotFoundError,IndexError):
            showErr("Unable to fetch last used wallpaper, setting entire history")
            with open(history_path, "w") as fl:
                fl.write("")

def resetDownloaded() -> None:
    try:
        with open(history_path, "r") as f:
            hist = f.readlines()
            wallInd=getConf("internal", "wall_index")
            if wallInd!=None:
                lastUsed = hist[int(wallInd)]
            else:
                lastUsed = ""

        toRemove = []
        wallDir=getConf("internet", "wallpaper_save_directory")
        if wallDir!=None:
            for img in listdir(wallDir):
                if img not in lastUsed:
                    toRemove.append(
                        path.join(wallDir, img)
                    )
            for i in toRemove:
                remove(i)
        else:
            showErr("Couldn't find wallpaper_save_directory in your config, so deleting nothing...")
    except (FileNotFoundError, IndexError):
        wallDir=getConf("internet", "wallpaper_save_directory")
        if wallDir!=None:
            for img in listdir():
                remove(path.join(getConf("internet", "wallpaper_save_directory"), img))
        else:
            showErr("Couldn't find wallpaper_save_directory in your config, so deleting nothing...")

def deleteLast() -> None:
    try:
        with open(history_path, "r") as f:
            hist = f.readlines()
            wallInd=getConf("internal", "wall_index") 
            if wallInd!=None:
                ind = int(wallInd) - 1
                lastUsed = hist[ind].replace("\n", "")
                hist.pop(ind)
                remove(lastUsed)
            else:
                showErr("Couldn't find the last wallpaper, unable to delete :(")
        a = ""
        for i in hist:
            a += i # newline character already included
        with open(history_path, "w") as f:
            f.write(a)

        print("Done!")
    except (FileNotFoundError, IndexError):
        showErr("Unable to delete, maybe its no longer in the history, or the history doesn't exist...")


def appendHistory(p: str) -> None:
    if path.isfile(history_path):
        try:
            with open(history_path, "r") as fl:
                a = fl.readlines()
                last = a[-1]
                limit=getConf("wallpaper", "wallpaper_history_limit")
                Ind=getConf("internal", "wall_index")
                if limit!=None and Ind!=None:
                    if len(a) >= int(limit):
                        resetHistory(int(Ind), nothing=True)
                else:
                    showErr("Couldn't read wallpaper_history_limit, or wall_index")
        except IndexError:
            last = ""

        try:
            with open(history_path, "a") as f:
                if p + "\n" != last:
                    f.write(p + "\n")
        except FileNotFoundError:
            showErr("Couldn't save to history, history file doesn't exist!")


## Additional functionalities ##=========================================================================================


def sendNotif(path: str) -> None:
    heading = getConf("triggers", "notif_message")
    body = getConf("triggers", "notif_body")
    if heading!=None or body!=None:
        body=body.replace(":f:", path)
        run(f"""notify-send "{heading}" "{body}" """, shell=True, capture_output=False)
    else:
        showErr("Couldn't find either of notif_body, or notif_message")


def runOnChange() -> None:
    cmd = getConf("triggers", "command")
    if cmd != "" or cmd!= None:
        run(cmd, shell=True, capture_output=False)
    else:
        c.print(
            "[red underline]Warning[/red underline]: Check your configuration plz, either disable command_on_change or set a valid command!"
        )

## Wallpaper related functions ##========================================================================================

def applyEffect(imgPath:str,save_path:str) -> None:
    t=getConf("effects","type").lower()
    try:
        from PIL import Image, ImageEnhance, ImageFilter
        img=Image.open(imgPath)

        if t=="blur":
            res=img.filter(ImageFilter.BLUR)
        elif t=="rank_filter":
            res=img.filter(ImageFilter.RankFilter(getConf("effects","rank_filter_size"),getConf("effects","rank_filter_rank")))
        elif t=="contour":
            res=img.filter(ImageFilter.CONTOUR)
        elif t=="detail":
            res=img.filter(ImageFilter.DETAIL)
        elif t=="emboss":
            res=img.filter(ImageFilter.EMBOSS)
        elif t=="sharpen":
            res=img.filter(ImageFilter.SHARPEN)
        elif t=="min_filter":
            res=img.filter(ImageFilter.MinFilter(getConf("effects","min_filter_size")))
        elif t=="max_filter":
            res=img.filter(ImageFilter.MaxFilter(getConf("effects","max_filter_size")))
        elif t=="smooth":
            res=img.filter(ImageFilter.SMOOTH)
        elif t=="smooth_more":
            res=img.filter(ImageFilter.SMOOTH_MORE)
        elif t=="box_blur":
            res=img.filter(ImageFilter.BoxBlur(radius=getConf("effects","box_blur_radius")))
        elif t=="median_blur":
            res=img.filter(ImageFilter.MedianFilter(getConf("effects","median_blur_size")))
        elif t=="grayscale":
            res=img.convert("L")
        elif t=="dim":
            res=ImageEnhance.Brightness(img).enhance(getConf("effects","dim_amount"))
        else:
            res=img.filter(ImageFilter.GaussianBlur(radius=getConf("effects","gaussian_blur_radius")))
        
        res.save(save_path)

    except ImportError:
        showErr("Pillow module is not installed! You need to install it to use this feature!")


def getPalette(amount=4, save_palette=False, general_palette=False) -> None:
    try:
        from colorthief import ColorThief
        fl = showCurrent(show_error=True)
        if fl!=None:
            img = ColorThief(fl)
            c.print("[bold yellow]Generating palette...[/bold yellow]")
            palette = img.get_palette(color_count=amount)

            c.print("[bold green]Done![/bold green]")

            for i in palette:
                h = rgbToHex(i)
                c.print(h, style=f"{h}")

            if save_palette:
                writePalette(palette)
                c.print("[green]Saved palette![/green]")

            if general_palette:
                writePalette(palette, general=True)
                c.print("[green]Saved general palette![/green]")

    except ImportError:
        showErr(
            "colorthief module is not installed! You need to install it to use this feature!"
        )


def chooseRandom(directory: str, more=[]) -> Union[None, str]:
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

    if allItems != []:
        return choice(allItems)
    else:
        return None


def setRandom(config, use_internet=False, use_down=False) -> None:
    if use_internet:
        q = getConf("internet", "image_query")
        if q == "" or q==None:
            c.print("[yellow]Warning: [/yellow] No image query mentioned in config file, searching for 'landscape' pics ")
            try:
                d = Downloader("landscape", source=returnSource())
                d.download(count=1)
                setWall(d.images[0])
            except:
                showErr("You either don't have an active internet connection, or you're making too many requests together!")
        else:
            try:
                d = Downloader(q, source=returnSource())
                d.download(count=1)
                setWall(d.images[0])
            except:
                showErr("You either don't have an active internet connection, or you're making too many requests together!")
    elif use_down:

        if config["internet"]["use_saved"]:
            wallDir=config["internet"]["wallpaper_save_directory"]
            if wallDir!=None:
                moreDirs = [wallDir]
            else:
                moreDirs = []
        else:
            moreDirs = []

        # randomWall = chooseRandom("", more=moreDirs)
        randomWall = chooseRandom(moreDirs[0], [])
        if randomWall == None:
            c.print("[yellow bold]Warning[/yellow bold]: Found no proper images, fetching from the internet...")
            setRandom(config, use_internet=True)
        else:
            config["internal"]["wall_index"] = -1
            setConf(config)
            setWall(randomWall)

    else:
        if config["internet"]["use_saved"]:
            wallDir=config["internet"]["wallpaper_save_directory"]
            if wallDir!=None:
                moreDirs = [wallDir]
            else:
                moreDirs = []
        else:
            moreDirs=[]

        wallD=config["wallpaper"]["wallpaper_directory"]
        if wallD!=None:
            randomWall = chooseRandom(
                wallD, more=moreDirs
            )
        else:
            showErr("wallpaper_directory is not set! please set that up")
            randomWall=None

        if randomWall == None:
            print("Found no proper images, fetching from the internet...")
            setRandom(config, use_internet=True)
        else:
            setWall(randomWall)
            config["internal"]["wall_index"] = -1
            setConf(config)


def setWall(p: str, save=True) -> None:
    p = path.abspath(p)

    if path.isfile(p):
        if getConf("effects","enabled"):
            d=getConf("effects","edited_wallpaper_directory")
            if d==None or d=="":

                c.print("[yellow bold]Warning[/yellow bold]: edited_wallpaper_directory not found, using ~/Pictures/easyfeh/edited")
                d=path.expanduser("~/Pictures/easyfeh/edited")
            
            p_name=path.splitext(path.basename(p))
            newImg=path.join(d,p_name[0]+"_modified."+p_name[1])
            applyEffect(p,newImg)
            p=newImg

        if getConf("other", "enabled"):
            cmd = getConf("other", "cmd").replace(":f:", p)
            run(f"{cmd}", shell=True, capture_output=False)
        else:

            if getenv("XDG_SESSION_TYPE") == "x11":
                options = getConf("feh", "options")
                run(f"feh {options} {p}", shell=True, capture_output=False)
            else:
                options = getConf("swww", "options")
                run(f"swww img {p} {options}", shell=True, capture_output=False)

        if save and getConf("wallpaper", "remember_wallpaper"):
            appendHistory(p)

        c.print("[green]Done! Wallpaper has been set:)[/green]")

        if getConf("triggers", "notify_on_change"):
            sendNotif(p)

        if getConf("palette","autogenerate_palette"):
            getPalette(4, general_palette=True)

        if getConf("triggers", "command_on_change"):
            runOnChange()


    else:
        showErr(
            "Invalid file, Are you sure that its an image? or if it even exists?"
        )


## Printing functions ##========================================================================================


def printHistory() -> None:
    global c
    try:
        with open(history_path, "r") as f:
            allStuff = f.readlines()
            l = len(allStuff)
            for ind, i in enumerate(allStuff):
                if ind == (l + getConf("internal", "wall_index")):
                    c.print(i.replace("\n", ""), r"[blue bold](Current)[/blue bold]")
                else:
                    print(i, end="")
            c.print("[blue]Total wallpapers in history: [/blue]", l)
    except:
        showErr(
            "Wasn't able to fetch history, are you sure history is turned on in the config file?"
        )


def listInstalled() -> None:
    try:
        saveDir = getConf("internet", "wallpaper_save_directory")
        count = 0
        if saveDir!=None and path.exists(saveDir): 
            for i in listdir(saveDir):
                print(path.join(saveDir, i))
                count += 1
            c.print("\n[blue]Total downloaded wallpapers: [/blue]", count)
        else:
            showErr(
                "Wasn't able to fetch the wallpapers... are you sure that the directory is configured properly in the config file?"
            )

    except:
        showErr(
            "Wasn't able to fetch the wallpapers... are you sure that the directory is configured properly in the config file?"
        )


def showCurrent(show_error=True) -> Union[str,None]:
    try:
        with open(history_path, "r") as f:
            Ind=getConf("internal", "wall_index")
            if Ind!=None:
                curr = f.readlines()[int(Ind)].replace(
                    "\n", ""
                )
                return curr
            else:
                if show_error:
                    showErr(
                        "Wallpaper not found, are you sure that wallpaper history is turned on?"
                    )
                return None

    except (FileNotFoundError,IndexError):
        if show_error:
            showErr(
                "Wallpaper not found, are you sure that wallpaper history is turned on?"
            )
        return None
