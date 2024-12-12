import RPi.GPIO as GPIO
import time

# Define the GPIO pins connected to the IR sensors
IR_PINS = [26, 17, 27, 22, 23, 24, 4]

# Set GPIO mode
GPIO.setmode(GPIO.BCM)  # Use BCM numbering

# Set up the IR sensor pins as inputs with pull-up resistors
for pin in IR_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def detect_column():
    """Detects which column (if any) has a piece inserted."""
    for i, pin in enumerate(IR_PINS):
        if GPIO.input(pin) == GPIO.LOW:  # IR sensor is active when LOW
            return i + 1  # Return the column number (1-7)
    return None  # No column detected

try:
    while True:
        detected_column = detect_column()
        if detected_column:
            print(f"Piece detected in column: {detected_column}")
            time.sleep(0.5)  # Debounce: Wait briefly to avoid multiple detections
        #time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()  # Clean up GPIO settings on exit