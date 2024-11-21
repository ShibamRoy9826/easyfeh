"""
This file contains most of the variables that easyfeh uses
"""

from os import getlogin, listdir, makedirs, mkdir, path
from toml import load,dump

username = getlogin()
config_ = f"/home/{username}/.config"
config_directory = config_ + "/easyfeh"
config_path = config_directory + "/config.toml"
history_path = config_directory + "/history.txt"
default_config = f"""
[wallpaper]
wallpaper_directory= "/home/{username}/Pictures"
random = false # sets random wallpapers from wallpaper_directory
remember_wallpaper = true # Saves to history 
wallpaper_history_limit = 50 # history limit, history resets automatically once this limit exceeds

[internet]
use_from_internet = false
image_source = "wallhaven" # "wallhaven"(default) or "unsplash"
wallpaper_save_directory = "/home/{username}/Pictures/easyfeh"
image_query = "landscape" # Search for images you want, default is "landscape" 
shuffle_results = true # Recommended, else, it will always lead to the same result(The first search result) , only valid for unsplash results
wallhaven_purity = "sfw" # Only if wallhaven is selected as image source. Options: "sfw", "nsfw"
use_saved = true # Also includes already downloaded images from the internet when -random is called

[triggers]
notify_on_change = false # sends a notification on wallpaper change
command_on_change = false # runs a command on wallpaper change, you can use it to run scripts
notif_message = "Wallpaper Changed!" # Notification heading (only if notify_on_change is turned on)
notif_body = "Wallpaper has been set to :f: " # Notification body (only if notify_on_change is turned on), :f: get's replaced by the image's path
command = "" # Set only if command_on_change is turned on

[feh]
options = "--bg-fill" # Feh options

[swww]
# Only if you're using wayland
options = ""

[other]
enabled = false
# If you want to use something other than feh or swww
cmd = ""
# Example: command -options :f: 
#    :f: get's replaced by the image path

[internal]
# Current Wallpaper index in the history
wall_index = -1
"""


helpTxt = r"""
[bold blue]EasyFeh[/bold blue]
[bold]__________[/bold]

[bold underline]Typical Usage:[/bold underline] [red]easyfeh -\[option] \[img_path(if required)][/red]

[bold underline]Commands:[/bold underline]
    [bold]easyfeh -h[/bold]
    or [bold]easyfeh -help[/bold]         [green]-> Prints this help message[/green]

    [bold]easyfeh -restore[/bold]
    or [bold]easyfeh -res[/bold]          [green]-> Sets the wallpaper which was last used [/green](Sets random if no history is saved,
                                needs random to be enabled in that case)

    [bold]easyfeh -prev[/bold]            
    or [bold]easyfeh -p[/bold]            [green]-> Sets previous wallpaper[/green] (requires wallpaper history to be turned on)

    [bold]easyfeh -next[/bold]            
    or [bold]easyfeh -n[/bold]            [green]-> Sets next wallpaper[/green] (requires wallpaper history to be turned on)

    [bold]easyfeh -random[/bold]          
    or [bold]easyfeh -r[/bold]            [green]-> Sets a random wallpaper[/green] (directory for random wallpaper must be configured 
                                or internet wallpapers should be turned on)

    [bold]easyfeh -random[/bold]          
            [bold]-use-internet[/bold] 
    or [bold]easyfeh -r -ui[/bold]        [green]-> Sets a random wallpaper from the internet[/green]

    [bold]easyfeh -random[/bold]          
            [bold]-use-down[/bold]
    or [bold]easyfeh -r -ud[/bold]        [green]-> Sets a random wallpaper from wallpapers downloaded from internet[/green]

    [bold]easyfeh \[some_img_path][/bold]  [green]-> Sets an image as wallpaper [/green]
                                (supported formats : jpg, jpeg, png, pnm, tiff, bmp, gif)

    [bold]easyfeh -reset-hist[/bold]      
    or [bold]easyfeh -rh[/bold]           ->  [red underline]WARNING![/red underline][green] Resets the wallpaper history [/green](Keeps the last used wallpaper,Take backups before running this!) 

    [bold]easyfeh -reset-walls[/bold]     
    or [bold]easyfeh -rw[/bold]           -> [red underline]WARNING![/red underline][green] Deletes all wallpapers downloaded from internet[/green] (Take backups before running this!)

    [bold]easyfeh -reset-conf[/bold]      
    or [bold]easyfeh -rc[/bold]           -> [red underline]WARNING![/red underline][green] Deletes Existing configuration and resets to default[/green] (Take backups before running this!)
    
    [bold]easyfeh -show-hist[/bold]      
    or [bold]easyfeh -sh[/bold]           -> [green]Prints out the history[/green]

    [bold]easyfeh -show-down[/bold]      
    or [bold]easyfeh -sd[/bold]           -> [green]Prints out all the wallpapers downloaded from internet[/green] (If any)

    [bold]easyfeh -show-curr[/bold]       
    or [bold]easyfeh -sc[/bold]           -> [green]Prints out the path to the current wallpaper[/green] (last used, requires wallpaper history to be turned on)

    [bold]easyfeh -download [blue]<amount>[/blue] [/bold]      -> [green]Downloads wallpapers[/green] (Doesn't set them)
    [bold]-query [blue]<query>[/blue] -source [blue]<source>[/blue][/bold]        Optional arguments : -query , -source
    or                                     If not specified, it will check the configuration.
    [bold]easyfeh -d [blue]<amount>[/blue] -q [blue]<query>[/blue][/bold]         Available options for sources: wallhaven, unsplash 
        [bold]-s [blue]<source>[/blue][/bold] 


[bold red]The configuration file for easyfeh can be found at $HOME/.config/easyfeh/config.toml[/bold red]
"""

supported_formats = [
    "bmp",   
    "jpeg", 
    "jpg", 
    "png",
    "gif",   
    "tiff",
    "tif",
    "ppm",   
    "pgm",  
    "pbm", 
    "pnm",
    "xbm",   
    "xpm",  
    "webp",
    "heif",  
    "heic"  
]

## Create Config if it doesn't exist ##==============================================================

def generateConf():
    if not "easyfeh" in listdir(config_):
        mkdir(config_+ "/easyfeh")
        with open(config_path, "w") as f:
            f.write(default_config)
        with open(path.join(config_directory, "history.txt"), "w") as f:
            pass

    else:
        if not path.isfile(config_path):
            with open(config_path, "w") as f:
                f.write(default_config)
        if not path.isfile(history_path):
            with open(history_path, "w") as f:
                pass

def generateWallDirs():
    with open(config_path,"r") as f:
        c=load(f)
    saveWall=c["internet"]["wallpaper_save_directory"]
    allWall=c["wallpaper"]["wallpaper_directory"]
    if not path.exists(saveWall):
        makedirs(saveWall,exist_ok=True)
    if not path.exists(allWall):
        makedirs(allWall,exist_ok=True)

generateConf()
generateWallDirs()

