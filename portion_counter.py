import RPi.GPIO as GPIO
import time

portion = 2

def count():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        last_value = GPIO.input(24)
        i = 0
        while i != (portion*2):
                #print(last_value)
                value = GPIO.input(24)
                #print(value)
                if value != last_value:
                	last_value = value
                	i += 1
                else:
                	pass
                time.sleep(0.1)

        return 0
