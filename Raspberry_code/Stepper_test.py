import RPi.GPIO as GPIO
import time

# Define GPIO pins
STEP_PIN = 16  # Step control
DIR_PIN = 20   # Direction control
ENABLE_PIN = 21  # Enable motor

# Constants
STEPS_PER_REV = 400  # Steps per revolution
REVOLUTIONS = 3      # Number of revolutions
DELAY = 0.0001
microstepping = 8

# GPIO setup
GPIO.setwarnings(False)  # Suppress GPIO warnings
GPIO.setmode(GPIO.BCM)   # Use Broadcom pin numbering
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(ENABLE_PIN, GPIO.OUT)

# Enable the motor driver
GPIO.output(ENABLE_PIN, GPIO.LOW)  # LOW to enable the motor driver

try:
    while True:
        # Rotate 3 revolutions in one direction
        print("Rotating 3 revolutions clockwise...")
        GPIO.output(DIR_PIN, GPIO.HIGH)  # Set direction to clockwise
        for _ in range(STEPS_PER_REV * REVOLUTIONS):
            GPIO.output(STEP_PIN, GPIO.HIGH)
            time.sleep(DELAY)  # Pulse duration
            GPIO.output(STEP_PIN, GPIO.LOW)
            time.sleep(DELAY)  # Delay between steps

        time.sleep(1)  # Pause before changing direction

        # Rotate 3 revolutions in the opposite direction
        print("Rotating 3 revolutions counterclockwise...")
        GPIO.output(DIR_PIN, GPIO.LOW)  # Set direction to counterclockwise
        for _ in range(STEPS_PER_REV * REVOLUTIONS):
            GPIO.output(STEP_PIN, GPIO.HIGH)
            time.sleep(DELAY)  # Pulse duration
            GPIO.output(STEP_PIN, GPIO.LOW)
            time.sleep(DELAY)  # Delay between steps

        time.sleep(1)  # Pause before the next cycle
except KeyboardInterrupt:
    print("Test interrupted by user.")
finally:
    GPIO.output(ENABLE_PIN, GPIO.HIGH)  # Disable the motor driver
    GPIO.cleanup()  # Release GPIO pins
    print("GPIO cleaned up.")
