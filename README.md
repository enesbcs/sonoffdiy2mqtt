# sonoffdiy2mqtt
Sonoff DIY mode devices to MQTT bridge
(Sonoff Basic R3 and Sonoff Mini)

# Installation
```
sudo apt install python3-pip 
git clone https://github.com/enesbcs/sonoffdiy2mqtt.git
cd sonoffdiy2mqtt
sudo pip3 install paho-mqtt requests zeroconf
python3 sonoffdiy2mqtt.py
```
# Usage
At first run without much configuration the sonoffdiy2mqtt.py will write out to the console to the Sonoff DIY plug ID's that it found through mDNS.

1/
In the "sonoffdiy2mqtt.json" file the default mode is "mqtt_type": "domoticz".
The Sonoff Device ID (ten character hexadecimal) has to be added to the "sonoff_device_id" fields and its correspondent Domoticz Dummy device IDX has to be added in the same line to the "outlet0" field.

Necessarry Domoticz Hardwares: "MQTT Client Gateway with Lan interface" and "Dummy"

2/
There are an other mode, if inside the "sonoffdiy2mqtt.json" file the "mqtt_type": "shelly" is setted then the sonoffdiy2mqtt script translates incoming mDNS messages to Shelly API compatible MQTT messages and paths, which can be intercepted by the Domoticz hardware "Shelly MQTT". ( https://github.com/enesbcs/Shelly_MQTT ) 

In this mode IDX is not required, but make sure to enable device self-learning.

# Earlier Sonoff Device LAN mode support
https://github.com/enesbcs/sonofflan2mqtt

| PayPal |
|-------|
|  [![donate](https://img.shields.io/badge/donate-PayPal-blue.svg)](https://www.paypal.me/rpieasy) |
If you like this project, or you wants to support the development, you can do that with the paypal link above or by doing pull requests, if you knew Python language.
[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/I3I5UT4H)
