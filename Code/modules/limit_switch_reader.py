import RPi.GPIO as GPIO
import time

# GPIO pin configuration
LIMIT_SWITCH_LEFT = 5   # GPIO pin for left limit switch
LIMIT_SWITCH_RIGHT = 6  # GPIO pin for right limit switch

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(LIMIT_SWITCH_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Enable pull-up resistor
GPIO.setup(LIMIT_SWITCH_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Enable pull-up resistor

def read_limit_switches():
    """
    Reads the states of the left and right limit switches.

    Returns:
        tuple: (left_switch_state, right_switch_state)
            - 1 if pressed (LOW state)
            - 0 if not pressed (HIGH state)
    """
    left_switch_state = 1 if GPIO.input(LIMIT_SWITCH_LEFT) == GPIO.LOW else 0
    right_switch_state = 1 if GPIO.input(LIMIT_SWITCH_RIGHT) == GPIO.LOW else 0
    return left_switch_state, right_switch_state