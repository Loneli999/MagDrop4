import RPi.GPIO as GPIO

# GPIO pin configuration
MOSFET_GATE_PIN = 10

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOSFET_GATE_PIN, GPIO.OUT)

def control_electromagnet(state):
    """
    Turns the electromagnet ON or OFF based on the input state.

    Parameters:
        state (bool): True to turn ON the electromagnet, False to turn it OFF.
    """
    if state:
        GPIO.output(MOSFET_GATE_PIN, GPIO.HIGH)  # Turn ON the electromagnet
        #print("Electromagnet is ON.")
    else:
        GPIO.output(MOSFET_GATE_PIN, GPIO.LOW)  # Turn OFF the electromagnet
        #print("Electromagnet is OFF.")