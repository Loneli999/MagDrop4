import RPi.GPIO as GPIO
import time

# Define GPIO pins
STEP_PIN = 16  # Step control
DIR_PIN = 20   # Direction control
ENABLE_PIN = 21  # Enable motor

# GPIO setup
GPIO.setmode(GPIO.BCM)   # Use Broadcom pin numbering
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(ENABLE_PIN, GPIO.OUT)

# Enable the motor driver
GPIO.output(ENABLE_PIN, GPIO.LOW)  # LOW to enable the motor driver
GPIO.output(DIR_PIN, GPIO.HIGH)   # Set direction (doesn't matter for holding)

try:
    print("Motor holding...")
    while True:
        # Keep the motor driver enabled and idle
        time.sleep(1)  # Sleep to keep the script running
except KeyboardInterrupt:
    print("Exiting motor hold...")
finally:
    GPIO.output(ENABLE_PIN, GPIO.HIGH)  # Disable the motor driver
    GPIO.cleanup()  # Release GPIO pins
    print("GPIO cleaned up.")
