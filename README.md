# EasyFeh 

A straight-forward & user-friendly wrapper originally meant for [feh](https://github.com/derf/feh), but works with any other wallpaper engine too!

written with ❤️ in Python :)

## Features 😎

- A wallpaper history , allows you to move forward or backward in history
- Highly customizable
- Allows users to fetch wallpapers from [unsplash](https://unsplash.com/) and [wallhaven](https://wallhaven.cc/)
- Also works in wayland but uses [swww](https://github.com/LGFae/swww) instead of feh by default
- Users can use any other wallpaper engine if they don't want to use swww or feh

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

## Demo 
[My Post On r/unixporn](https://www.reddit.com/r/unixporn/comments/1guwilk/oc_created_a_wallpaper_managing_application/)

## Dependencies

The dependencies include: 

- [feh](https://github.com/derf/feh)

- [swww](https://github.com/LGFae/swww) (Optional, only if you're on wayland)

- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

- [toml](https://pypi.org/project/toml/)

- [requests](https://pypi.org/project/requests/)

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
```

<h2>
    Usage <img src="https://github.com/Anmol-Baranwal/Cool-GIFs-For-GitHub/assets/74038190/7b282ec6-fcc3-4600-90a7-2c3140549f58" width="30">
</h2>

Here's a list of all the commands (Updated as of the latest commit)
```text
EasyFeh
__________

Typical Usage: easyfeh -[option] [img_path(if required)]

Commands:
    easyfeh -h
    or easyfeh -help         -> Prints this help message

    easyfeh -restore
    or easyfeh -res          -> Sets the wallpaper which was last used (Sets random if no history is saved,
                                needs random to be enabled in that case)

    easyfeh -prev            
    or easyfeh -p            -> Sets previous wallpaper (requires wallpaper history to be turned on)

    easyfeh -next            
    or easyfeh -n            -> Sets next wallpaper (requires wallpaper history to be turned on)

    easyfeh -random          
    or easyfeh -r            -> Sets a random wallpaper (directory for random wallpaper must be configured 
                                or internet wallpapers should be turned on)

    easyfeh -random          
            -use-internet 
    or easyfeh -r -ui        -> Sets a random wallpaper from the internet

    easyfeh -random          
            -use-down
    or easyfeh -r -ud        -> Sets a random wallpaper from wallpapers downloaded from internet

    easyfeh [some_img_path]  -> Sets an image as wallpaper 
                                (supported formats : jpg, jpeg, png, pnm, tiff, bmp, gif)

    easyfeh -reset-hist      
    or easyfeh -rh           ->  WARNING! Resets the wallpaper history (Keeps the last used wallpaper,Take backups before running this!) 

    easyfeh -reset-walls     
    or easyfeh -rw           -> WARNING! Deletes all wallpapers downloaded from internet (Take backups before running this!)

    easyfeh -reset-conf      
    or easyfeh -rc           -> WARNING! Deletes Existing configuration and resets to default (Take backups before running this!)
    
    easyfeh -show-hist      
    or easyfeh -sh           -> Prints out the history

    easyfeh -show-down      
    or easyfeh -sd           -> Prints out all the wallpapers downloaded from internet (If any)

    easyfeh -show-curr       
    or easyfeh -sc           -> Prints out the path to the current wallpaper (last used, requires wallpaper history to be turned on)

    easyfeh -download <amount>       -> Downloads wallpapers (Doesn't set them)
    -query <query> -source <source>        Optional arguments : -query , -source
    or                                     If not specified, it will check the configuration.
    easyfeh -d <amount> -q <query>         Available options for sources: wallhaven, unsplash 
        -s <source> 

```

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

## To-Do 🛠️
- Fetch wallpapers faster with wallhaven API
- Option for API keys
- Configuration verifier
- Easy to switch wallpaper collections/themes
- Wallpaper effects (blur, dim ,etc..)
- A rust variant of the same project :) (Might take some time, I am learning about rust now)

## Known bugs 🐞
- Get's the same wallpaper sometimes when it tries to set random wallpapers

## Contributing 🤝

Everyone is welcome to contribute to the code!

You can also raise an issue, or suggest any features that you think would be great :)

> ✨ Please star this repository if you liked this project 😁
