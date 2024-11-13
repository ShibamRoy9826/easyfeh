"""
This file contains most of the variables that easyfeh uses
"""

from os import getlogin, listdir, mkdir, path

username = getlogin()
config_ = f"/home/{username}/.config"
config_directory = config_ + "/easyfeh"
config_path = config_directory + "/config.toml"
history_path = config_directory + "/history.txt"
default_config = f"""
[wallpaper]
wallpaper_directory= "/home/{username}/Pictures"
random = false
remember_wallpaper = true
wallpaper_history = 50

[internet]
use_from_internet = false
image_source = "unsplash" # For now this is the only option
wallpaper_save_directory = "/home/{username}/Pictures/easyfeh"
image_query = "landscape" # Search for images you want, default is "landscape" 
shuffle_results = true # Recommended, else, it will always lead to the same result(The first search result)

[feh]
options = "--bg-fill"

[swww]
# Only if you're using wayland
options = ""

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
                                that case)
    easyfeh -prev            -> Sets previous wallpaper (requires wallpaper history to be turned on)
    easyfeh -next            -> Sets next wallpaper (requires wallpaper history to be turned on)
    easyfeh -random          -> Sets a random wallpaper (directory for random wallpaper must be configured or internet wallpapers should be 
                                turned on)
    easyfeh -random          -> Sets a random wallpaper from the internet
            -use-internet       
    easyfeh [some_img_path]  -> Sets an image as wallpaper (supported formats : jpg, jpeg, png, pnm, tiff, bmp, gif)
    easyfeh -reset-hist      -> Resets the wallpaper history (Keeps the last used wallpaper)
    easyfeh -reset-walls     -> Deletes all wallpapers downloaded from internet
    easyfeh -show-hist       -> Prints out the history
    easyfeh -reset-conf      -> WARNING! Deletes Existing configuration and resets to default (Take backups before running this!)

** The configuration file for easyfeh can be found at $HOME/.config/easyfeh/config.toml **
** Please avoid using multiple options for now, it should work, but may be buggy        **
"""

## Create Config if it doesn't exist ##==============================================================

if "easyfeh" not in listdir(config_directory):
    mkdir(config_directory + "/easyfeh")
    if not path.isfile(config_path):
        with open(config_path, "w") as f:
            f.write(default_config)
    if not path.isfile(path.join(config_directory, "history.txt")):
        with open(path.join(config_directory, "history.txt"), "w") as f:
            pass

else:
    if not path.isfile(config_path):
        with open(config_path, "w") as f:
            f.write(default_config)
    if not path.isfile(path.join(config_directory, "history.txt")):
        with open(path.join(config_directory, "history.txt"), "w") as f:
            pass
