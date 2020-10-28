import os, glob,importlib.util
import sys
import getopt


def getDirFormEnv():
    return os.getenv('IOTPY_DEVICES_DIR')

def getDirFromArg(argv):
    opts = []
    try:
        opts, args = getopt.getopt(argv,"d:",["dir="])
    except :
        pass
    for opt, arg in opts:
        if opt in ("-d", "--dir"):
            print("Reading Devices from Dir: ", arg)
            return arg
    return None

def loadDevices():
    DIR = getDirFormEnv()
    if DIR is None:
        DIR = getDirFromArg(sys.argv[1:])
    if DIR is None:
        print("Devices directory not specified. Quit...")
        print("Usage:")
        print("\tiotpy --dir <absolute-path-to-dir>")
        print("OR with env variable like below:")
        print("\texport IOTPY_DEVICES_DIR=<absolute-path-to-dir>")
        sys.exit(2)
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

