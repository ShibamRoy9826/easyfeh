# EasyFeh

A straight-forward & user-friendly wrapper for [feh](https://github.com/derf/feh), written in Python :)


## Features

- A wallpaper history , allows you to move forward or backward in history
- Highly customizable
- Allows users to fetch wallpapers from [unsplash](https://unsplash.com/) and [wallhaven](https://wallhaven.cc/)
- Also works in wayland but uses [swww](https://github.com/LGFae/swww) instead of feh

## Dependencies

The dependencies include: 

- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

- [toml](https://pypi.org/project/toml/)

- [requests](https://pypi.org/project/requests/)

Although the dependencies will be automatically installed while installing the application, if you still want to install these dependencies manually, you can checkout the `requirements.txt` file. and run `pip install -r requirements.txt`


## Installation


You can install EasyFeh by cloning this repository locally and install it using pip.
Here's the command:
```bash
git clone https://github.com/ShibamRoy9826/easyfeh.git
cd easyfeh
pip install .
```


## Usage/Examples

Here's a list of all the commands
```bash
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
    easyfeh -reset-conf      -> WARNING! Deletes Existing configuration and resets to default (Take backups before running this!)
    easyfeh -show-hist       -> Prints out the history
    easyfeh -show-installed  -> Prints out all the wallpapers installed from internet (If any)
    easyfeh -show-current    -> Prints out the path to the current wallpaper(last used, requires wallpaper history to be turned on)

    easyfeh -download <amount>      -> Downloads wallpapers(Doesn't set them)
    -query <query> -source <source>    Optional arguments : -query , -source
                                       If not specified, it will check the configuration.
                                       Available options for sources: unsplash, wallhaven

```


## Configuration

The configuration file for EasyFeh can be found at `$HOME/.config/easyfeh/config.toml`

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

[internal]
# Current Wallpaper index in the history
wall_index = -1
```
## To-Do
- Easy to switch wallpaper collections/themes
- Wallpaper effects (blur, dim ,etc..)
- A rust variant of the same project :) (Might take some time, I am learning about rust now)

## Known bugs
- Get's the same wallpaper sometimes when it tries to set random wallpapers

## Contributing

Everyone is welcome to contribute to the code!

You can also raise an issue, or suggest any features that you think would be great :)
