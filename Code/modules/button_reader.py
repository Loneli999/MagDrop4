import RPi.GPIO as GPIO
import time

# Define GPIO pins for buttons
RED_BUTTON = 13
BLUE_BUTTON = 19

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BLUE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def read_buttons():
    red_button_state = 1 if GPIO.input(RED_BUTTON) == GPIO.LOW else 0
    blue_button_state = 1 if GPIO.input(BLUE_BUTTON) == GPIO.LOW else 0
    return red_button_state, blue_button_state
