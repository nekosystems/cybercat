import importlib
import os

scene_list = []

for _module in os.listdir(os.path.dirname(__file__)):
    if _module == "__init__.py" or _module[-3:] != ".py": continue
    print ("Importing scene " + _module[:-3] + " from " + __name__)
    scene_list.append(importlib.import_module("." +  _module[:-3], __name__))
del _module