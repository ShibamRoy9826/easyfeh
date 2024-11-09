"""
This file contains most of the variables that easyfeh uses
"""

from os import getlogin, path

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
use_from_internet = false # Uses Images from Unsplash
cached_wallpaper_directory = "/home/{username}/Pictures/easyfeh"

[feh]
options="--bg-fill"

[swww]
# Only if you're using wayland
options=""

[internal]
# Current Wallpaper index in the history
wall_index=-1
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
    easyfeh [some_img_path]  -> Sets an image as wallpaper (supported formats : jpg, jpeg, png, pnm, tiff, bmp, gif)
    easyfeh -reset-hist      -> Resets the wallpaper history (Keeps the last used wallpaper)
    easyfeh -reset-walls     -> Deletes all wallpapers downloaded from internet
    easyfeh -show-hist       -> Prints out the history
    easyfeh -reset-conf      -> WARNING! Deletes Existing configuration and resets to default (Take backups before running this!)

** The configuration file for easyfeh can be found at $HOME/.config/easyfeh/config.toml **
** Please avoid using multiple options for now, it should work, but may be buggy        **
"""
