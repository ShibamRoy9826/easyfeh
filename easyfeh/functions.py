## Modules
from os import getenv, listdir, remove, walk
from random import choice
from subprocess import run

from rich.console import Console

from .conf import *
from .webscraper import Downloader

c = Console()

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
    with open(config_path, "r") as f:
        config = load(f)
    return config[section][var]


def returnSource() -> int:
    return int(getConf("internet", "image_source").lower() != "unsplash")


def returnSourceParam(param: str) -> int:
    return int(param.lower() != "unsplash")


def resetHistory(index: int, nothing=False) -> None:
    if nothing:
        with open(history_path, "w") as fl:
            fl.write("")
    else:
        with open(history_path, "r") as f:
            last = f.readlines()[index]
        with open(history_path, "w") as fl:
            fl.write(last)


def resetDownloaded() -> None:
    try:
        with open(history_path, "r") as f:
            hist = f.readlines()
            lastUsed = hist[int(getConf("internal", "wall_index"))]
        toRemove = []
        for img in listdir(getConf("internet", "wallpaper_save_directory")):
            if img in lastUsed:
                pass
            else:
                toRemove.append(
                    path.join(getConf("internet", "wallpaper_save_directory"), img)
                )
        for i in toRemove:
            remove(i)
    except (FileNotFoundError, IndexError):
        for img in listdir(getConf("internet", "wallpaper_save_directory")):
            remove(path.join(getConf("internet", "wallpaper_save_directory"), img))


def deleteLast() -> None:
    try:
        with open(history_path, "r") as f:
            hist = f.readlines()
            ind = int(getConf("internal", "wall_index")) - 1
            lastUsed = hist[ind].replace("\n", "")
            hist.pop(ind)
            remove(lastUsed)
        a = ""
        for i in hist:
            a += i
        with open(history_path, "w") as f:
            f.write(a)
        print("Done!")
    except:
        c.print(
            "[red]Error:[/red] unable to delete, maybe its no longer in the history..."
        )


def appendHistory(p: str) -> None:
    if path.isfile(history_path):
        try:
            with open(history_path, "r") as fl:
                a = fl.readlines()
                last = a[-1]
                if len(a) >= int(getConf("wallpaper", "wallpaper_history_limit")):
                    resetHistory(int(getConf("internal", "wall_index")), nothing=True)
        except IndexError:
            last = ""
        with open(history_path, "a") as f:
            if p + "\n" != last:
                f.write(p + "\n")


## Additional functionalities ##=========================================================================================


def sendNotif(path: str) -> None:
    heading = getConf("triggers", "notif_message")
    body = getConf("triggers", "notif_body").replace(":f:", path)
    run(f"""notify-send "{heading}" "{body}" """, shell=True, capture_output=False)


def runOnChange() -> None:
    cmd = getConf("triggers", "command")
    if cmd != "":
        run(cmd, shell=True, capture_output=False)
    else:
        c.print(
            "[red underline]Warning[/red underline]: Check your configuration plz, either disable command_on_change or set a valid command!"
        )



## Wallpaper related functions ##========================================================================================

def applyEffect(imgPath:str,save_path:str) -> None:
    t=getConf("effects","type").lower()

    try:
        from PIL import Image, ImageFilter,ImageEnhance
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
        c.print("[bold red]Error:[/bold red] Pillow module is not installed! You need to install it to use this feature!")



    


def getPalette(amount=4, save_palette=False, general_palette=False) -> None:
    try:
        from colorthief import ColorThief

        fl = showCurrent(show_error=False)
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
        c.print(
            "[bold red]Error:[/bold red] colorthief module is not installed! You need to install it to use this feature!"
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
        if q == "":
            d = Downloader("landscape", source=returnSource())
            d.download(count=1)
            setWall(d.images[0])
        else:
            d = Downloader(q, source=returnSource())
            d.download(count=1)
            setWall(d.images[0])
    elif use_down:
        if config["internet"]["use_saved"]:
            moreDirs = [config["internet"]["wallpaper_save_directory"]]
        else:
            moreDirs = []

        randomWall = chooseRandom("", more=moreDirs)
        if randomWall == None:
            print("Found no proper images, fetching from the internet...")
            setRandom(config, use_internet=True)
        else:
            config["internal"]["wall_index"] = -1
            setConf(config)
            setWall(randomWall)

    else:
        if config["internet"]["use_saved"]:
            moreDirs = [config["internet"]["wallpaper_save_directory"]]
        else:
            moreDirs = []

        randomWall = chooseRandom(
            config["wallpaper"]["wallpaper_directory"], more=moreDirs
        )
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
            p_name=p.split("/")[-1].split(".")
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

        print("Done! Wallpaper has been set:)")

        if getConf("triggers", "notify_on_change"):
            sendNotif(p)

        if getConf("palette","autogenerate_palette"):
            getPalette(4, general_palette=True)

        if getConf("triggers", "command_on_change"):
            runOnChange()


    else:
        c.print(
            "[bold red]Error:[/bold red] Invalid filetype, Are you sure that its an image?"
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
        c.print(
            "[red]Error:[/red] Wasn't able to fetch history, are you sure history is turned on in the config file?"
        )


def listInstalled() -> None:
    try:
        saveDir = getConf("internet", "wallpaper_save_directory")
        count = 0
        for i in listdir(saveDir):
            print(path.join(saveDir, i))
            count += 1
        c.print("\n[blue]Total downloaded wallpapers: [/blue]", count)
    except:
        c.print(
            "[red]Error:[/red] Wasn't able to fetch the wallpapers... are you sure that the directory is configured properly in the config file?"
        )


def showCurrent(show_error=True) -> Union[str,None]:
    try:
        with open(history_path, "r") as f:
            curr = f.readlines()[int(getConf("internal", "wall_index"))].replace(
                "\n", ""
            )
            return curr
    except:
        if show_error:
            c.print(
                "[red]Error:[/red] Wallpaper not found, are you sure that wallpaper history is turned on?"
            )
        return None
