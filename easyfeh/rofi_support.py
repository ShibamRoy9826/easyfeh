from os import walk,path
from subprocess import run
from .conf import config_path,supported_formats
from toml import load

with open(config_path,"r") as f:
    config=load(f)
directory = config["wallpaper"]["wallpaper_directory"]
more =[config["internet"]["wallpaper_save_directory"]]

allItems = []
flStr=""

if path.exists(directory):
    for dirpath, _, filenames in walk(directory):
        for filename in filenames:
            if filename.endswith(tuple(supported_formats)):
                allItems.append((path.join(dirpath, filename),filename))
                flStr+=filename+"="

for i in more:
    if path.exists(i):
        for dirpath, _, filenames in walk(i):
            for filename in filenames:
                if filename.endswith(tuple(supported_formats)):
                    allItems.append((path.join(dirpath, filename),filename))
                    flStr+=filename+"="


def runRofi():
    opt=run(f"echo {flStr} | rofi -dmenu -sep '=' -dmenu -i -format 's'",shell=True,capture_output=True)
    o=opt.stdout.decode("utf-8").replace("\n","")
    for p,f in allItems:
        if f==o:
            print(p,f)




runRofi()
