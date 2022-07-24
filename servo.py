import RPi.GPIO as GPIO
import time
from portion_counter import count

class Motor:
	def __init__(self):
		self.motor_user_id = None
	def start(self, id):
		if self.motor_user_id == id:
			GPIO.setmode(GPIO.BCM) 
			GPIO.setup(18 ,GPIO.OUT)
			GPIO.output(18, True)
			print("start") 
			count()
			print("stop")
			GPIO.output(18, False)
			return 0
		else:
			return 1 

	def claim(self, id):
		if self.motor_user_id == None:
			self.motor_user_id = id
			return 0
		else:
			return 1

	def release(self, id):
		if id == self.motor_user_id:
			self.motor_user_id = None
		#time.sleep(10800)
			return 0
		else:
			return 1

