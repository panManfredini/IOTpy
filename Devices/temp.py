from Device import Device, addDevice


class test(Device):
    def init(self):
        self.addVariable("test0")
        self.addVariable("test1")

    def loop(self):
        self.setVariableValue("test0", 1)
        self.setVariableValue("test1", 2)

    def write(self, name, val):
        pass

    def cleanup(self):
        pass


t = test()
t.loop()
addDevice(t)
print("added device")
