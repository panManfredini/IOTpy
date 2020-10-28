# IOTpy
Framework to expose IOT devices trough REST API and Prometheus metrics. Perfect for Raspberry Pi.

- You write your script to comunicate with the device
- Define the variables that you want to expose 
- And IOTpy publishes those variables via REST API and Prometheus metrics

# Installation
```bash
git clone https://github.com/panManfredini/IOTpy
cd IOTpy
pip install .
```
# Usage
```bash
iotpy --dir <absolute-path-to-dir> --port <port-number>

# OR with env variable like below:
export IOTPY_DEVICES_DIR=<absolute-path-to-dir>
export IOTPY_DEVICES_PORT=<port-number>
```
With `dir` is intended the directory where your `device` files are stored (see below for more info).

# Run the Example
```bash
# After installation and in the cloned folder
cd example
export IOTPY_DEVICES_DIR=$(pwd)
iotpy
```
Now visit [http://localhost:8085](http://localhost:8085).


# How does it work
IOTpy is a webserver that loads dynamically the code you place in a predefined directory, it extracts all the 
variables devined in those `devices` files and exposes them trough an HTTP API and Prometheus metrics.

**What is a Device?** For `device` is intended a class that inherits from the abstrac class `iotpy.Device.Device`. After you inherit the class, you must implement
four methods: `init` where you initialize your device (for example open a serial connection) and define the variables, `loop` is a function that is automatically called
every `n` seconds (where `n` is configurable, default is 2) where you can poll your device and update the variables value. 
In the `write` method you execute an HTTP write request (somebody, trough the API has asked to write a value to the device), 
the method is called only if the device has defined that variable (so no need to double check), here you ask your device to set that variable then return 
`True` if success and `False` otherwise, if you cant write on the device just return always `False`.
Finally the `cleanup` method is used to gracefully shutdown the system, here for example, you close the serial connection with your device.

**How define/set/read a device variable?** The `device` class already has methods implemented for that and these are `addVariable`, `setVariableValue`, `readVariableValue`.

**Minimal example:** you find a little more complete example [here](https://github.com/panManfredini/IOTpy/blob/main/example/exampleDevice.py).

```python
from iotpy.Device import Device, addDevice

class myDevice(Device):

    def init(self):
        # here initialize your device connection...

        # adding a variables to the system
        self.addVariable("test0", "test variable")
        self.addVariable("test1")

        # call loop every 2 sec
        self.poll_loop_ms = 2000


    def loop(self):
        # here poll your device

        # and save variables values
        self.setVariableValue("test0", Value0)
        self.setVariableValue("test1", Value1)

    def write(self, name, val):
        # here execute write request on your device
        
        # and set variable value
        self.setVariableValue(name, val)

        return True  # False for failure

    def cleanup(self):
        # do some cleanup, for example close connection with device
        pass



#IMPORTANT: You must create and add the device to the list
addDevice( myDevice("test") )
```

**Run the system:** Now you just need to place all your devices files in a directory and run the IOTpy server with the absolute path to your dir.
```
iotpy --dir <path-to-your-dir>
```
An now you can visit [http://localhost:8085](http://localhost:8085) and check from the `dev panel` if your device is working correctly.

# The API

The server has three routes:
- `/` where a simple control panel is
- `/variables` returns a JSON object with all defined variables and their current values, in the format. `{"varName":varValue}`
- `/metrics` return the Prometheus metrics of your variable, you need to point Prometheus to this URL.
- `/restart` this shutdow gracefully the server, **Note:** only if you defined the iotpy to run as a daemon then it will be restarted automatically.

