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

# Run the Example
```bash
cd example
export IOTPY_DEVICES_DIR=$(pwd)
iotpy
```
Now visit [http://localhost:8085](http://localhost:8085).

# How does it work



