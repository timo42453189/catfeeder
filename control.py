import threading
import smbus
import os
from detect import AutoDetect
from servo import Motor
from file_control import FileControl
from mqtt import Mqtt
import motion
import webserver


def start_api():
	os.system("uvicorn api:app --port 5000 --host 192.168.178.46 --log-level critical")

addr = 0x8
bus = smbus.SMBus(1)
bus.write_byte(addr, 0x1)

m = Motor()

ai = AutoDetect(m)
file_handler = FileControl(m)
mqtt_client = Mqtt(m)

def create_threads(p):
        t = []
        for i in p:
                t.append(threading.Thread(target=i, args=()))
        return t

p = [ai.detect, file_handler.check_file, start_api, mqtt_client.start, motion.start, webserver.start]
t = create_threads(p)

for i in t:
	i.start()

bus.write_byte(addr, 0x2)

for i in t:
	i.join()

