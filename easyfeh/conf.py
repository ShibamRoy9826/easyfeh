"""
This file contains most of the variables that easyfeh uses
"""

from os import getlogin, listdir, makedirs, path
from typing import Union

from toml import dump, load

version = "v0.1.4 (2nd release)"
username = getlogin()
config_ = f"/home/{username}/.config"
config_directory = config_ + "/easyfeh"
config_path = config_directory + "/config.toml"
history_path = config_directory + "/history.txt"
default_config = f"""
[wallpaper]
wallpaper_directory= "/home/{username}/Pictures"
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
use_api = false # Not recommended, but is an option if you have an api key (Only for wallhaven) 
wallhaven_api_key = "" # Only required if "use_api" is set to true

[triggers]
notify_on_change = false # sends a notification on wallpaper change
command_on_change = false # runs a command on wallpaper change, you can use it to run scripts
notif_message = "Wallpaper Changed!" # Notification heading (only if notify_on_change is turned on)
notif_body = "Wallpaper has been set to :f: " # Notification body (only if notify_on_change is turned on), :f: get's replaced by the image's path
command = "" # Set only if command_on_change is turned on

[palette]
save_palette = true  # Saves the requested palette from -gc command, to a txt file, where each line is in the format: (R,G,B)       #hex
palette_path = "/home/{username}/.config/easyfeh/palette.txt" # Where to keep the newly generated palette?
dominant_color_quality = 6 # (10 is highest, and 1 is the least, smaller values take less time, but at a cost of quality)
general_palette_copy = true # Generates another copy of the palette with values like fg, bg, primary, and secondary
complete_palette_path = "/home/{username}/.config/easyfeh/full_palette.txt" # Where to store the newly generated complete palette?
autogenerate_palette = false # Automatically create a palette on wallpaper change

[effects]
enabled= false
type="gaussian_blur" # Available options include "gaussian_blur", "blur","grayscale","rank_filter","sharpen","contour","detail","emboss","min_filter","max_filter","smooth","smooth_more","box_blur","median_filter"

## No need to change if you're not using any of these effects 
gaussian_blur_radius = 8
rank_filter_size = 3
rank_filter_rank = 1
min_filter_size = 3
max_filter_size = 3
box_blur_radius = 8
median_blur_size = 5
dim_amount = 0.5
edited_wallpaper_directory = "/home/{username}/Pictures/easyfeh"

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
    "heic",
]

## Create Config if it doesn't exist ##==============================================================


def generateConf() -> None:
    if not "easyfeh" in listdir(config_):
        makedirs(config_+"/easyfeh")
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


def generateWallDirs() -> None:
    with open(config_path, "r") as f:
        c = load(f)
    saveWall = c["internet"]["wallpaper_save_directory"]
    allWall = c["wallpaper"]["wallpaper_directory"]
    if not path.exists(saveWall):
        makedirs(saveWall, exist_ok=True)
    if not path.exists(allWall):
        makedirs(allWall, exist_ok=True)


generateConf()
generateWallDirs()
