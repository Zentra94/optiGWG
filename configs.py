from pathlib import Path
import os

PATH_MAIN = Path(os.path.dirname(__file__))
PATH_DATA = PATH_MAIN / "data"
PATH_DATA_INPUT = PATH_DATA / "input"
PATH_DATA_OUTPUT = PATH_DATA / "output"
PATH_DATA_MODELS = PATH_DATA / "models"
PATH_DATA_PLOTS = PATH_DATA / "plots"
PATH_NOTEBOOKS = PATH_MAIN / "notebooks"
PATH_STATICS = PATH_MAIN / "statics"
PATH_STATICS_IMAGES = PATH_STATICS / "images"
PATH_STATICS_GLOBALS = PATH_STATICS / "globals"
PATH_UTILS = PATH_MAIN / "utils"

if __name__ == '__main__':
    print("the main path is: {}".format(PATH_MAIN))
    vars = locals().copy()
    paths = {}
    for k, v in vars.items():
        if k.startswith("PATH_"):
            path = Path(v)
            if path.is_dir():
                print("directory {} already exists".format(v))
            else:
                os.mkdir(path)
                print("directory {} created".format(v))
