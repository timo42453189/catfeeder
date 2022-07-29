import logging
import time

from error import error_handler

class FileControl:
	def __init__(self, m):
		self.id = 2
		#logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a', format='%(filename)s - %(asctime)s - %(levelname)s - %(message)s')
		with open("servo_control.txt", "w") as f:
			f.write("0")
			f.close()
		self.motor = m

	def check_file(self):
		error_handler("File control startet", "info")
		while True:
			f = open("servo_control.txt", "r")
			content = f.read()
			#print(content)
			if int(content) == 1:
				error_handler("Motor started manually with file control", "info")
				f = open("servo_control.txt", "w")
				f.write("0")
				response = self.motor.claim(self.id)
				if response == 1:
					error_handler("Motor already in use", "error")
				else:
					self.motor.start(self.id)
					self.motor.release(self.id)
			f.close()
			time.sleep(1)
