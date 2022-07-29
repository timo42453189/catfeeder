import logging
import smbus
import time


logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a', format='%(filename)s - %(asctime)s - %(levelname)s - %(message)s')

addr = 0x8
bus = smbus.SMBus(1)

def error_handler(error, level):
	if level == "info":
		logging.info(error)
	if level == "error":
		logging.error(error)
		bus.write_byte(addr, 0x1)
		time.sleep(1)
		bus.write_byte(addr, 0x2)
	return 0
