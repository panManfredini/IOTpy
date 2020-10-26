import os, glob,importlib.util

print("IOTpy Initialization. Loading Devices:")
DIR = os.getenv('IOTPY_DEVICES_DIR')

if DIR[-1] == '/' :
    DIR = DIR[0:-1]

for path in glob.glob(DIR+'/[!_]*.py'):
    name, ext = os.path.splitext(os.path.basename(path))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    print("   ---->Successfully loaded Device module '", name, "' from:", path)
