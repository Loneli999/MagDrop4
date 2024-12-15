import RPi.GPIO as GPIO

# IR sensor pins
IR_PINS = [26, 17, 27, 22, 23, 24, 4]

# GPIO setup
GPIO.setmode(GPIO.BCM)
for pin in IR_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def read_ir_sensors(ignore_sensors=[]):
    triggered_sensors = []

    for index, pin in enumerate(IR_PINS):
        sensor_number = index + 1
        if sensor_number in ignore_sensors:
            continue  # Skip ignored sensors

        if GPIO.input(pin) == GPIO.LOW:
            triggered_sensors.append(index + 1)

    if len(triggered_sensors) == 1:
        return triggered_sensors[0]  # Return the single triggered sensor number
    else:
        return None  # No sensors or more than one sensor triggered
