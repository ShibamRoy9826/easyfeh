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

