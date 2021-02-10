from iotpy.Device import Device, addDevice
from random import Random

class testDevice(Device):

    def __init__(self,name):
        # You need to call constructor of Device
        Device.__init__(self,name)

        self.rand = Random()
        # adding a variables to the system
        self.addVariable("test0", "test variable")
        self.addVariable("test1")
        self.addVariable("alwais_fail")

        # call loop every 2 sec
        self.poll_loop_ms = 2000

        # here initialize your device connection
        # open serial connection for example...

    def loop(self):
        # here poll your device
        # and save variables values
        self.setVariableValue("test0", self.rand.random())
        self.setVariableValue("test1", self.rand.random())
        # status 0 and 1 are reserved, you can use status > 2
        self.setVariableStatus("alwais_fail", 2,"UKNOWN FAILURE")
        
    def write(self, name, val):
        # here execute write request
        # and set variable value
        self.setVariableValue(name, val)

        # return True if success, False otherwise
        # if your device is not writable, return always false
        return True

    def cleanup(self):
        # do some cleanup, for example close connection with device
        print("stopping device gracefully...")



#IMPORTANT: You must create and add the device to the list
addDevice( testDevice("test") )

