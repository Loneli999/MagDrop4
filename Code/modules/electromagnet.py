import RPi.GPIO as GPIO

MOSFET_GATE_PIN = 10
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOSFET_GATE_PIN, GPIO.OUT)

def control_electromagnet(state):
    if state:
        GPIO.output(MOSFET_GATE_PIN, GPIO.HIGH)  # Turn ON
    else:
        GPIO.output(MOSFET_GATE_PIN, GPIO.LOW)  # Turn OFF