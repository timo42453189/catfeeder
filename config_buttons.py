import RPi.GPIO as GPIO
import smbus
import time
from error import error_handler

addr = 0x8
bus = smbus.SMBus(1)

class Button:
	def __init__(self, m):
		self.portion = int(open("portion.conf", "r").read())
		self.available_pins = {"Motor": "26", "Up": "20", "Ok": "16"}
		self.led_mapping = {"1": 0x5, "2": 0x6, "3": 0x7, "4": 0x8}
		GPIO.setmode(GPIO.BCM)
		self.motor = m
		self.id = 4

	def check(self):
		while True:
			for i in self.available_pins:
				GPIO.setup(int(self.available_pins.get(i)), GPIO.IN, pull_up_down=GPIO.PUD_UP)
				val = GPIO.input(int(self.available_pins.get(i)))
				if val == 0:
					if i == "Motor":
						error_handler("Motor started manually with Button", "info")
						response = self.motor.claim(self.id)
						if response == 1:
							error_handler("Motor already in use", "error")
						else:
							self.motor.start(self.id)
							self.motor.release(self.id)
					if i == "Up":
						if self.portion + 1 > 4:
							self.portion = 4
						else:
							self.portion += 1
						data = self.led_mapping[f"{self.portion}"]
						with open("portion.conf", "w") as f:
							f.write(str(self.portion))
							f.close()
						bus.write_byte(addr, data)
						time.sleep(0.2)
						bus.write_byte(addr, 0x2)

					if i == "Ok":
						if self.portion -1 < 1:
							self.portion = 1
						else:
							self.portion = self.portion - 1
						data = self.led_mapping[f"{self.portion}"]
						with open("portion.conf", "w") as f:
							f.write(str(self.portion))
							f.close()
						bus.write_byte(addr, data)
						time.sleep(0.2)
						bus.write_byte(addr, 0x2)
