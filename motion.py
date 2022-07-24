import RPi.GPIO as io
import smbus
import time
from error import error_handler

io.setmode(io.BCM)
io.setup(23, io.IN)

addr = 0x8
bus = smbus.SMBus(1)

def start():
	while True:
		sensor = io.input(23)
		if sensor == 1:
			error_handler("Motion detected", "info")
			bus.write_byte(addr, 0x0)
			time.sleep(30)
			bus.write_byte(addr, 0x2)
		time.sleep(1)
