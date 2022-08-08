import logging
import paho.mqtt.client as mqtt
import time

from error import error_handler


class Mqtt:
	def __init__(self, m):
		self.motor = m
		self.id = 3
		self.broker_address = "test.mosquitto.org"
		try:
			self.topic = str(open("mqtt.conf", "r").read())
			self.topic = self.topic.replace("\n", "")
		except FileNotFoundError:
			error_handler("No mqtt config found", "error")
			raise FileNotFoundError("No mqtt config found")
			exit()
		self.client = mqtt.Client("timo")
		self.client.on_message = self.on_message
		self.client.connect(self.broker_address)
		#logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a', format='%(filename)s - %(asctime)s - %(levelname)s - %(message)s')
		error_handler("Mqtt service started", "info")

	def start(self):
		self.client.loop_start()
		self.client.subscribe(self.topic)
		while True:
			pass
		self.client.loop_stop()

	def on_message(self, client, userdata, message):
		message= str(message.payload.decode("utf-8"))
		#print(message)
		if message == "true":
			error_handler("Motor started manually from mqtt", "info")
			response = self.motor.claim(self.id)
			if response == 1:
				error_handler("Motor already in use", "error")
			else:
				self.motor.start(self.id)
				self.motor.release(self.id)
			client.publish(self.topic, "false")



