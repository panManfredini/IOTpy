import importlib
import glob
import os
import sys
from .readArgs import getDirAndPort

def loadDevices():
    DIR, PORT = getDirAndPort()
    
    print("IOTpy Initialization. Loading Devices:")
    if DIR[-1] == '/' :
        DIR = DIR[0:-1]
    
    loaded_modules = []
    for path in glob.glob(DIR+'/[!_]*.py'):
        name, ext = os.path.splitext(os.path.basename(path))
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        loaded_modules.append(mod)
        print("\tSuccessfully loaded Device module '", name, "' from:", path)
    if len(loaded_modules) == 0:
        print("\tError: no Device found in dir: ", DIR)
        sys.exit()

