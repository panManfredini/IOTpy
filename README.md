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

In the [Example](https://github.com/panManfredini/IOTpy/tree/main/example) folder, there is a simple device you can start with. This creates a `device` that exposes two variables `test0` and `test1`, 
which are populated with randomly generated variable values.

```bash
# After installation and in the cloned folder
cd example
export IOTPY_DEVICES_DIR=$(pwd)
iotpy
```
Now visit [http://localhost:8085](http://localhost:8085).


# How does it work
IOTpy is a webserver that loads dynamically the `devices` you place in a predefined directory, it extracts all the 
variables defined in those `devices` files and exposes them trough an HTTP API and Prometheus metrics.

**What is a Device?** For `device` is intended a class that inherits from the abstrac class `iotpy.Device.Device`. After you inherit the class, you must implement
four methods: 
- `init` where you initialize your device (for example open a serial connection) and define the variables, 
- `loop` is a function that is automatically called every `n` seconds (where `n` is configurable, default is 2) where you can poll your device and update the variables value. 
- In the `write` method you execute an HTTP write request (somebody, trough the API has asked to write a value to the device), the method is called only if the device has defined that variable (so no need to double check), here you ask your device to set that variable then return `True` if success and `False` otherwise, if your device is read-only the just return always `False`.
- Finally the `cleanup` method is used to gracefully shutdown the system, here for example, you close the serial connection with your device.

**How does the IOTpy know about variables and when they change?**  The `device` class has methods implemented to interact with IOTpy server's variables, these are `addVariable`, `setVariableValue` and `readVariableValue`. 

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

# The HTTP API URLs

The server has a few defined URL routes:

| Route | HTTP Method | Notes |  
|--------|-------------|------------|
|`/`| GET | returns a simple control panel. |  
|`/variables`| GET | returns a JSON object with all defined variables and their current values, in the format. `{"varName":varValue}` |  
|`/metrics` | GET | return the Prometheus metrics of your variable, you need to point Prometheus to this URL. |  
|`/write` | POST | this route is used to request a variable value change, JSON payload is required in the format `{"name":"varName","value":varValue}`. |  
|`/restart`| GET | this shutdow gracefully the server, **Note:** only if you defined the iotpy to run as a daemon then it will be restarted automatically.|


# Run IOTpy as a service (on linux)

These instruction only work on OS which uses `systemd` (so ubuntu for example). 
First you need to edit [this file](https://github.com/panManfredini/IOTpy/blob/main/iotpy.service) changing the command to run `iotpy` according to your system.

```bash
# find where is your iotpy is installed 
which iotpy
# change permission
chmod u+x <path-to-iotpy>

# Edit this line of iotpy.service file
    ExecStart=<path-to-iotpy>/iotpy --dir <path-to-devices> --port 8085

# Save file into systemd directory
sudo cp iotpy.service /etc/systemd/system/.

# Start service 
sudo systemctl start iotpy
# Get info
sudo systemctl status iotpy
# Stop 
sudo systemctl stop iotpy
# Restart
sudo systemctl restart iotpy

# Enable service at startup
sudo systemctl enable iotpy

```

# Powered by

Many thanks to:

- Twisted
- Milligram.css 
- Prometheus 

And to the `University of Zurich` for support to this project.
