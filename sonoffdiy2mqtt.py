#!/usr/bin/env python3
#############################################################################
####################### Sonoff DIY devices to MQTT bridge ###################
#############################################################################
#
# Copyright (C) 2019 by Alexander Nagy - https://bitekmindenhol.blog.hu/
#

from zeroconf import ServiceBrowser, Zeroconf # pip3 install zeroconf
from sonoffdiy import *
import sl2m_mqtt
import time
import sys, signal, os
import json

MQTT_TOPIC_PUB = ""
MQTT_TOPIC_SUB = ""

def signal_handler(signal, frame):
 sys.exit(0)

def mqtt_callback(did,val,outlet=0):
 global ssettings, listener
# print("From MQTT:",did,val,outlet)
 try:
  vval = int(val[0])
 except:
  vval = int(val)
 try:
  if ssettings["mqtt_type"]=="domoticz":
   for sondev in ssettings["device_idx_list"]:
    if int(sondev["idx"]["outlet0"])==int(did):
     sid = sondev["sonoff_device_id"]
     listener.setstate(sid,vval)
  else:
   listener.setstate(did,vval)
 except Exception as e:
    print("error:",str(e))

def sonoff_callback(devid,state,rssi,outlet=0):
 global mqttcontroller, ssettings
# print("From Sonoff: ",devid,state,rssi)
 if ssettings["mqtt_type"]=="domoticz":
  for sondev in ssettings["device_idx_list"]:
   if sondev["sonoff_device_id"]==devid:
    idx = int(sondev["idx"]["outlet0"])
    if idx>0:
     mqttcontroller.senddata(idx,state,rssi)
    break
 else:
  mqttcontroller.senddata2(devid,outlet,state)


signal.signal(signal.SIGINT, signal_handler)
try:
 os.chdir(os.path.dirname(os.path.realpath(__file__))) # go to our own directory
except:
 pass
try:
 with open("sonoffdiy2mqtt.json") as f:  # open config file
  ssettings = json.load(f)
except Exception as e:
 print("sonoffdiy2mqtt.json can not be read! ",str(e))
 ssettings = []
 sys.exit(1)
if ssettings["mqtt_type"]=="domoticz":
 se = False
else:
 se = True
zeroconf = Zeroconf()
listener = SonoffDIYListener(sonoff_callback,zeroconf,se)
browser = ServiceBrowser(zeroconf, "_ewelink._tcp.local.", listener)
#listener.startloop()

try:
 MQTT_TOPIC_PUB = ssettings["mqtt_topic_pub"].strip()
 MQTT_TOPIC_SUB = ssettings["mqtt_topic_sub"].strip()
 if ssettings["mqtt_type"]=="domoticz":
  if ssettings["mqtt_topic_pub"].strip()=="": # auto-fill with correct values if empty
   MQTT_TOPIC_PUB = "domoticz/in"
  if ssettings["mqtt_topic_sub"].strip()=="": # auto-fill with correct values if empty
   MQTT_TOPIC_SUB = "domoticz/out"
 if ssettings["mqtt_type"]=="shelly":         # auto-fill with correct values if empty
   MQTT_TOPIC_PUB = "shellies/"
   MQTT_TOPIC_SUB = "shellies/#"
 if ssettings["mqtt_address"]:
  mqttcontroller = sl2m_mqtt.Controller(ssettings["mqtt_address"],ssettings["mqtt_port"], ssettings["mqtt_type"],MQTT_TOPIC_PUB,MQTT_TOPIC_SUB,ssettings["mqtt_user"],ssettings["mqtt_password"])
  mqttcontroller.controller_init(True,mqtt_callback)
except Exception as e:
 print("MQTT setup failed",str(e))
 mqttcontroller = None
 sys.exit(0)

listener.bgloop()
#while True:
# time.sleep(1)
