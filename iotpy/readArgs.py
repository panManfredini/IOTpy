import os, glob,importlib.util
import sys
import getopt

def getDirFormEnv():
    return os.getenv('IOTPY_DEVICES_DIR')

def getDirAndPortFromArgs(argv):
    opts = []
    try:
        opts, args = getopt.getopt(argv,"hd:p:",["help","dir=","port="])
    except :
        pass
    
    DIR = None
    PORT = None
    for opt, arg in opts:
        if opt in ("-d", "--dir"):
            print("Reading Devices from Dir: ", arg)
            DIR = arg
        if opt in ("-p", "--port"):
            PORT = arg
        if opt in ("-h","--help"):
            printHelp()
            sys.exit()
    return DIR, PORT

def printHelp():
    print("Usage:")
    print("\tiotpy --dir <absolute-path-to-dir> --port <port-number>")
    print("OR with env variable like below:")
    print("\texport IOTPY_DEVICES_DIR=<absolute-path-to-dir>")
    print("\texport IOTPY_DEVICES_PORT=<port-number>")

def getPortFromEnv():
    return os.getenv('IOTPY_DEVICES_PORT')


def getDirAndPort():
    DIR, PORT = getDirAndPortFromArgs(sys.argv[1:])
    if DIR is None:
        DIR = getDirFormEnv()
    if DIR is None:
        printHelp()
        sys.exit(2)

    if PORT is None:
        PORT = getPortFromEnv()
    if PORT is None:
        PORT = 8085
    try:
        PORT = int(PORT)
    except:
        print("Bad Port")
        sys.exit(2)
    return DIR, PORT


