import abc
from prometheus_client import Gauge


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
    def __init__(self):
        self.variables = dict()
        self.init()

    def addVariable(self, name, description=""):
        self.variables[name] = PromVar(name, description)

    def getVariableValue(self, name):
        if self.variables.get(name) is not None:
            return self.variables[name].getValue()
        else:
            return None

    def setVariableValue(self, name, value):
        if self.variables.get(name) is not None:
            self.variables[name].setValue(value)

    def hasVar(self, name):
        return self.variables.get(name) is not None

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
