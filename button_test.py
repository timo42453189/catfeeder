import RPi.GPIO as GPIO
import time

# 20 -> UP
# 16 -> OK
# 26 -> SET


####################################
# CHECK REC AND PLAY BUTTON 
####################################
pin = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
	print(GPIO.input(pin))
	time.sleep(0.1)
