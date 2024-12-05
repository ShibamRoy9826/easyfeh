# EasyFeh 

A straight-forward & user-friendly wrapper originally meant for [feh](https://github.com/derf/feh), but works with any other wallpaper engine too!

written with ❤️ in Python :)

## Features 😎

- A wallpaper history , allows you to move forward or backward in history
- Highly customizable
- Allows users to fetch wallpapers from [unsplash](https://unsplash.com/) and [wallhaven](https://wallhaven.cc/)
- Also works in wayland but uses [swww](https://github.com/LGFae/swww) instead of feh by default
- Users can use any other wallpaper engine if they don't want to use swww or feh
- It can generated palettes from the current wallpaper

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

## What's New ❔

- It can now apply effects to your wallpaper such as dim, grayscale, blur,etc!
- Better outputs, coloured output is beautiful isn't it?
- An effects section in the config file, more power to the users :)

## Demo
[Drive Link](https://drive.google.com/file/d/1jQIqvLqMqC2AbFPMbpbQHRxuLqS5eNpg/view?usp=sharing)

## Dependencies

The dependencies include: 

- [feh](https://github.com/derf/feh)

- [swww](https://github.com/LGFae/swww) (Optional, only if you're on wayland)

- [pillow](https://github.com/python-pillow/Pillow) (Optional, only if you need wallpaper effects feature)

- [colorthief](https://github.com/fengsp/color-thief-py) (Optional, only if you want color palette generation)

- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

- [toml](https://pypi.org/project/toml/)

- [requests](https://pypi.org/project/requests/)

- [rich](https://github.com/Textualize/rich)

>[!NOTE]
> I know colorthief isn't maintained anymore, Its just there temporarily, and I will implement something of my own when i get the time for it

Although the dependencies will be automatically installed while installing the application, if you still want to install these dependencies manually, you can checkout the `requirements.txt` file. and run `pip install -r requirements.txt`
If you want to use something other than feh or swww, you can do that by enabling `other` in the configuration file, and setting the cmd parameter

<h2>
    Installation <img src="https://github.com/Anmol-Baranwal/Cool-GIFs-For-GitHub/assets/74038190/7b282ec6-fcc3-4600-90a7-2c3140549f58" width="30">
</h2>

If you're on Arch Linux, like me, then you can install it from the AUR:
```bash
paru -S easyfeh
```

There's also a development version to check out the latest changes:
```bash
paru -S easyfeh-git
```
Make sure to replace `paru` with whatever AUR helper you use.

For other distros try (installs locally to the user):
```bash
python setup.py install --user
```
if you want to install it systemwide, you can try:
```bash
sudo python setup.py install
```

If your distro allows python package installation directly using pip,
You can install EasyFeh by cloning this repository locally.
Here's the command:
```bash
git clone https://github.com/ShibamRoy9826/easyfeh.git
cd easyfeh
pip install .
```
That's it! read the usage of the commands and enjoy!

## Configuration 🛠️

The configuration file for EasyFeh can be found at `$HOME/.config/easyfeh/config.toml`

> [!NOTE]
> Its recommended to configure the wallpaper_directory so that its easier to set your desired wallpapers

Its well-commented with explaination of each parameter. Here's the default configuration file of EasyFeh

```text
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
```

<h2>
    Usage <img src="https://github.com/Anmol-Baranwal/Cool-GIFs-For-GitHub/assets/74038190/7b282ec6-fcc3-4600-90a7-2c3140549f58" width="30">
</h2>

Here's a list of all the commands (Updated as of the latest commit)
```text

EasyFeh
__________

Typical Usage: easyfeh -[option] [img_path(if required)]

╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ easyfeh -h     -> Prints this help message                                                                                                  │
│ or easyfeh --help                                                                                                                           │
│                                                                                                                                             │
│ easyfeh -v     -> Prints out app version                                                                                                    │
│ or easyfeh --version                                                                                                                        │
│                                                                                                                                             │
│ easyfeh <some_image_path>     -> Sets the wallpaper which was last used (Sets random if no history is saved, needs random to be enabled in  │
│ that case)                                                                                                                                  │
│                                                                                                                                             │
│ easyfeh -res     -> Sets the wallpaper which was last used (Sets random if no history is saved, needs random to be enabled in that case)    │
│ or easyfeh --restore                                                                                                                        │
│                                                                                                                                             │
│ easyfeh -p     -> Sets previous wallpaper (Requires wallpaper history to be turned on)                                                      │
│ or easyfeh --prev                                                                                                                           │
│                                                                                                                                             │
│ easyfeh -n     -> Sets next wallpaper (requires wallpaper history to be turned on)                                                          │
│ or easyfeh --next                                                                                                                           │
│                                                                                                                                             │
│ easyfeh -r     -> Sets a random wallpaper (directory for random wallpaper must be configured or internet wallpapers should be turned on)    │
│ or easyfeh --random                                                                                                                         │
│                                                                                                                                             │
│ easyfeh -r -ui       -> Sets a random wallpaper from the internet                                                                           │
│ or easyfeh --random --use-internet                                                                                                          │
│                                                                                                                                             │
│ easyfeh -r -ud       -> Sets a random wallpaper which is already downloaded from the internet                                               │
│ or easyfeh --random --use-internet                                                                                                          │
│                                                                                                                                             │
│ easyfeh -rh     -> WARNING Resets the wallpaper history  (Keeps the last used wallpaper,Take backups before running this!)                  │
│ or easyfeh --reset-hist                                                                                                                     │
│                                                                                                                                             │
│ easyfeh -rw     -> WARNING Deletes the wallpapers downloaded from internet (Take backups before running this!)                              │
│ or easyfeh --reset-walls                                                                                                                    │
│                                                                                                                                             │
│ easyfeh -rc     -> WARNING Deletes existing configuration and resets to default (Take backups before running this!)                         │
│ or easyfeh --reset-conf                                                                                                                     │
│                                                                                                                                             │
│ easyfeh -dl     -> WARNING Deletes last used wallpaper (Wallpaper before current, Take backups before running this!)                        │
│ or easyfeh --delete-last                                                                                                                    │
│                                                                                                                                             │
│ easyfeh -sh     -> Prints out history                                                                                                       │
│ or easyfeh --show-hist                                                                                                                      │
│                                                                                                                                             │
│ easyfeh -sd     -> Prints out all the wallpapers downloaded from internet (If any)                                                          │
│ or easyfeh --show-down                                                                                                                      │
│                                                                                                                                             │
│ easyfeh -sc     -> Prints out the path to the current wallpaper (last used, requires wallpaper history to be turned on)                     │
│ or easyfeh --show-curr                                                                                                                      │
│                                                                                                                                             │
│ easyfeh -gc <amount>      -> Prints out dominant colors from an image (RGB values)                                                          │
│                                                                                                                                             │
│ easyfeh -gd     -> Prints out the most dominant from an image (RGB values)                                                                  │
│ or easyfeh --get-dominant                                                                                                                   │
│                                                                                                                                             │
│ easyfeh -d     -> Download wallpapers(Doesn't set them)                                                                                     │
│ or easyfeh --download                                                                                                                       │
│                                                                                                                                             │
│ easyfeh -d <amount> -q <query> -s <source>       -> Download wallpapers (Doesn't set them)                                                  │
│ or easyfeh --query <query> --source <source>                                                                                                │
│                                                                                                                                             │
│ (Optional arguments: -q, -s ; If not specified, it will check configuration)(Source options: wallhaven(default), unsplash)                  │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

The configuration file for easyfeh can be found at $HOME/.config/easyfeh/config.toml
```

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

## To-Do 🛠️
- Fix Wallhaven API usage(It does'nt work well atm)
- Configuration verifier
- Easy to switch wallpaper collections/themes
- A rust variant of the same project :) (Might take some time, I am learning about rust now)

## Known bugs 🐞
- Get's the same wallpaper sometimes when it tries to set random wallpapers

## Contributing 🤝

Everyone is welcome to contribute to the code!

You can also raise an issue, or suggest any features that you think would be great :)

> ✨ Please star this repository if you liked this project 😁
