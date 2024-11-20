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
image_source = "unsplash" # "unsplash"(default) or "wallhaven"
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


helpTxt = """
EasyFeh
__________

Typical Usage: easyfeh -[option] [img_path(if required)]

Commands:
    easyfeh -h 
    or easyfeh -help         -> Prints this help message

    easyfeh -restore         -> Sets the wallpaper which was last used (Sets random if no history is saved, needs random to be enabled in 
    or easyfeh -res             that case)

    easyfeh -prev            -> Sets previous wallpaper (requires wallpaper history to be turned on)
    or easyfeh -p

    easyfeh -next            -> Sets next wallpaper (requires wallpaper history to be turned on)
    or easyfeh -n

    easyfeh -random          -> Sets a random wallpaper (directory for random wallpaper must be configured or internet wallpapers should be    or easyfeh -r               turned on)

    easyfeh -random          -> Sets a random wallpaper from the internet
            -use-internet       
    or easyfeh -r -ui

    easyfeh -random          -> Sets a random wallpaper from wallpapers downloaded from internet
            -use-down
    or easyfeh -r -ud

    easyfeh [some_img_path]  -> Sets an image as wallpaper (supported formats : jpg, jpeg, png, pnm, tiff, bmp, gif)

    easyfeh -reset-hist      -> Resets the wallpaper history (Keeps the last used wallpaper)
    or easyfeh -rh

    easyfeh -reset-walls     -> Deletes all wallpapers downloaded from internet
    or easyfeh -rw

    easyfeh -reset-conf      -> WARNING! Deletes Existing configuration and resets to default (Take backups before running this!)
    or easyfeh -rc
    
    easyfeh -show-hist       -> Prints out the history
    or easyfeh -sh

    easyfeh -show-down       -> Prints out all the wallpapers downloaded from internet (If any)
    or easyfeh -sd

    easyfeh -show-curr       -> Prints out the path to the current wallpaper(last used, requires wallpaper history to be turned on)
    or easyfeh -sc

    easyfeh -download <amount>      -> Downloads wallpapers(Doesn't set them)
    -query <query> -source <source>    Optional arguments : -query , -source
    or                                 If not specified, it will check the configuration.
    easyfeh -d <amount> -q <query>     Available options for sources: unsplash, wallhaven
        -s <source>                 


** The configuration file for easyfeh can be found at $HOME/.config/easyfeh/config.toml **
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

