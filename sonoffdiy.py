#############################################################################
####################### SonoffDIY management library#########################
#############################################################################
#
# Copyright (C) 2019 by Alexander Nagy - https://bitekmindenhol.blog.hu/
#
import time
import json
import threading
import requests # pip3 install requests

def parseAddress(address):
        add_list = []
        for i in range(4):
            add_list.append(int(address.hex()[(i*2):(i+1)*2], 16))
        add_str = str(add_list[0]) + "." + str(add_list[1]) + "." + str(add_list[2])+ "." + str(add_list[3])
        return add_str

def getstate(instate):
 s = str(instate).lower().strip()
 if s=="on" or s=="1":
  return 1
 else:
  return 0

switch_states = ['off','on']

class SonoffDIYListener:

    def __init__(self,handler=None,ozeroconf=None,sendwithecho=False):
      self.zeroconf = ozeroconf
      self.sendwithecho = sendwithecho
      self.devices = {}
      self.status = {}
      self.event_handler = handler
      self.run = True
 
    def getdevid(self,name):
      res = str(name)
      try:
       res = name[8:18]
      except:
       pass
      return res

    def remove_service(self, zeroconf, type, name):
        if name not in self.devices:
         return
        self.statechanged(self.getdevid(name),0,0)
        try:
         del self.devices[name]
        except:
         pass
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info.properties[b'type']==b'diy_plug':
         self.devices[name] = type
         self.status[name] = -1
         print("eWeLink DIY plug found: "+self.getdevid(name))
#         print("Service %s added, service info: %s" % (name, info))

    def statechanged(self,devid,state,battery,outlet=0):
#      print(devid," ",state," ",battery)
      if self.event_handler is not None:
       try:
        self.event_handler(devid,state,battery)
       except:
        pass

    def startloop(self):
     self.bg = threading.Thread(target=self.bgloop)
     self.bg.daemon = True
     self.run = True
     self.bg.start()

    def bgloop(self):
     while self.run:
      if len(self.devices)>0:
        for name,stype in self.devices.items():
         i = self.zeroconf.get_service_info(stype, name)
         if i is not None:
          try:
#           print(self.getdevid(name)," ",parseAddress(i.address)," ",i.port," ")
           data = json.loads(i.properties[b'data1'].decode())
#           print(data["switch"],data["rssi"])
           cstat = getstate(data["switch"])
           if cstat!=self.status[name]:
            self.status[name]=cstat
            self.statechanged(self.getdevid(name),cstat,int(data["rssi"]))
          except Exception as e:
           print(e)
      time.sleep(0.5)

    def stoploop(self):
     self.run = False

    def setstate(self,devid,state):
        for name,stype in self.devices.items():
         if "_"+str(devid)+"." in name:
          i = self.zeroconf.get_service_info(stype, name)
#          print(parseAddress(i.address),":",i.port)
          data = {}
          url = "http://" + parseAddress(i.address) + ":" + str(i.port) + "/zeroconf/switch" # create url for switching
          data["sequence"] = str(int(time.time()))
          data["deviceid"] = str(devid)
          if int(state)==1:                            # construct json dataset
                data["data"] = {"switch": "on"}
          else:
                data["data"] = {"switch": "off"}
          if self.sendwithecho==False:
           self.status[name]=int(state)
#          print(devid,state)
          self.send_data(send_url=url, send_data=data)

    def send_data(self, send_url, send_data):
       try:
        r = requests.post(send_url, json=send_data) # do POST call
       except:
        pass

