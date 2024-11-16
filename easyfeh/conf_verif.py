from .conf import *

def checkConf():
    if not "easyfeh" in listdir(config_):
        mkdir(config_directory)
        with open(config_path, "w") as f:
            f.write(default_config)
    else:
        if not path.isfile(config_path):
            with open(config_path, "w") as f:
                f.write(default_config)


