import os, glob,importlib.util

print("IOTpy Initialization. Loading Devices:")
for path in glob.glob('Devices/[!_]*.py'):
    name, ext = os.path.splitext(os.path.basename(path))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    print("   ---->Successfully loaded Device '", name, "' from module:", path)
