import abc
from prometheus_client import Gauge
from threading import Thread
import time

class PromVar:
    def __init__(self, name, description=""):
        self.name = name
        self.value = None
        self.prom = Gauge(name, description)

    def setValue(self, value):
        self.value = value
        self.prom.set(value)

    def getValue(self):
        return self.value


class Device(abc.ABC):
    def __init__(self, name):
        self.name = name
        #self.namespace_prefix = ""
        self.poll_loop_ms = 2000
        self.variables = dict()
        self._keep_running = True
        self.init()
        self._loop_thread = Thread(target=self._loop_handler, daemon=True)
        self._loop_thread.start()

    def addVariable(self, name, description=""):
        self.variables[name] = PromVar(name, description)

    def getVariableValue(self, name):
        if self.variables.get(name) is not None:
            return self.variables[name].getValue()
        else:
            return None

    def getAllVariablesValues(self):
        var_dict = dict()
        for key, value in self.variables.items():
            var_dict[key] = value.getValue()
        return var_dict

    def setVariableValue(self, name, value):
        if self.variables.get(name) is not None:
            self.variables[name].setValue(value)

    def hasVar(self, name):
        return self.variables.get(name) != None


    def _loop_handler(self):
        print("Starting Loop cycle for device", self.name)
        while self._keep_running:
            self.loop()
            time.sleep(self.poll_loop_ms / 1000)

    def is_alive(self):
        return self._loop_thread.is_alive()

    def stop(self):
        self._keep_running = False
        self.cleanup()

    @abc.abstractmethod
    def init(self):
        pass

    @abc.abstractmethod
    def loop(self):
        pass

    @abc.abstractmethod
    def write(self, name, value):
        """
        Parameters
        ----------
        name : str
            varibale name that has been requested 
        value : any
            variable value that has to be written
        """
        pass

    @abc.abstractmethod
    def cleanup(self):
        pass


listOfDevices = []


def addDevice(device):
    listOfDevices.append(device)


def getDeviceWithVar(name):
    device = None
    for dev in listOfDevices:
        if dev.hasVar(name):
            device = dev
            break
    return device