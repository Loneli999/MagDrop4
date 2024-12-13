import RPi.GPIO as GPIO
import time

# Define GPIO pins for buttons
RED_BUTTON = 13  # GPIO 13
BLUE_BUTTON = 19  # GPIO 19

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Enable pull-up resistor
GPIO.setup(BLUE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Enable pull-up resistor

def read_buttons():
    """
    Reads the red and blue buttons and returns their states.
    
    Returns:
        tuple: (red_button, blue_button)
            - red_button: 1 if pressed, 0 if not.
            - blue_button: 1 if pressed, 0 if not.
    """
    red_button_state = 1 if GPIO.input(RED_BUTTON) == GPIO.LOW else 0
    blue_button_state = 1 if GPIO.input(BLUE_BUTTON) == GPIO.LOW else 0
    return red_button_state, blue_button_state
