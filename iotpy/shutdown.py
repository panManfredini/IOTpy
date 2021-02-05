import signal
from .Device import listOfDevices
from twisted.internet import reactor
from threading import Thread
import time



def GracefullShutdown(sig, form):
    for device in listOfDevices:
            device.stop()
    t = Thread(target=server_shutdown)
    t.start()


def server_shutdown():
    time.sleep(0.3)
    reactor.stop()

def SetShutdownHandler():
    signal.signal(signal.SIGINT, GracefullShutdown)
    signal.signal(signal.SIGTERM, GracefullShutdown)