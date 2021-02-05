import abc
from prometheus_client import Gauge
from threading import Thread
import time
import signal

class PromVar:
    def __init__(self, name, description=""):
        self.name = name
        self.value = None
        self.description = description
        self.lastUpdate_ms = int(time.time() * 1000) 
        self.status = 0
        self.error = ""
        self.prom = Gauge(name, description)

    def setValue(self, value):
        self.value = value
        self.prom.set(value)
        self.status = 1
        self.lastUpdate_ms = int(time.time() * 1000)

    def setStatus(self, status, error=""):
        self.status = status
        self.error = error
    
    def getValue(self):
        return self.value
    
    def getVariableSummary(self):
        summary = dict()
        summary["name"] = self.name
        summary["value"] = self.getValue()
        summary["description"] = self.description
        summary["lastUpdate_ms"] = self.lastUpdate_ms
        summary["status"] = self.status
        summary["error"] = self.error
        return summary


class Device(abc.ABC):
    def __init__(self, name):
        self.name = name
        #self.namespace_prefix = ""
        self.poll_loop_ms = 2000
        self.variables = dict()
        self._keep_running = True
        self._loop_thread = Thread(target=self._loop_handler, daemon=True)

    def addVariable(self, name, description=""):
        self.variables[name] = PromVar(name, description)

    def getVariableValue(self, name):
        if self.variables.get(name) is not None:
            return self.variables[name].getValue()
        else:
            return None

    def getAllVariablesSummary(self):
        var_list = []
        for key, value in self.variables.items():
            var_list.append( value.getVariableSummary() )
        return var_list

    def setVariableValue(self, name, value):
        if self.variables.get(name) is not None:
            self.variables[name].setValue(value)

    def setVariableStatus(self, name, status, error=""):
        if self.variables.get(name) is not None:
            self.variables[name].setStatus(status, error)

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

def StartDevicesLoop():
    for dev in listOfDevices:
        try:
            dev._loop_thread.start()
            print("Started loop for device - ",dev.name)
        except:
            print("Failed to start loop for device - ",dev.name)
        
def getDeviceWithVar(name):
    device = None
    for dev in listOfDevices:
        if dev.hasVar(name):
            device = dev
            break
    return device
