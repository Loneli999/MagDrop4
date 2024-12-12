import spidev
import RPi.GPIO as GPIO
import time

# Pin configuration
RESET_PIN = 9  # Reset pin
SPI_CS_PIN = 8  # Chip Select

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI0, Chip Select 0
spi.max_speed_hz = 1000000  # 1 MHz

GPIO.setmode(GPIO.BCM)
GPIO.setup(RESET_PIN, GPIO.OUT)

def reset_display():
    GPIO.output(RESET_PIN, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(RESET_PIN, GPIO.HIGH)

def send_command(command):
    # Send a single command byte over SPI
    spi.xfer([command])

def send_data(data):
    # Send display data over SPI
    if isinstance(data, list):
        spi.xfer(data)  # Send a list of bytes
    else:
        spi.xfer([data])  # Send a single byte

def oled_init():
    reset_display()
    send_command(0x2A)  # Function set (extended command set)
    send_command(0x71)  # Function selection A
    send_data(0x00)     # Disable internal VDD regulator
    send_command(0x28)  # Function set (fundamental command set)
    send_command(0x08)  # Display off
    send_command(0x2A)  # Function set (extended command set)
    send_command(0x79)  # OLED command set enabled
    send_command(0xD5)  # Set display clock divide ratio/oscillator frequency
    send_command(0x70)  # Set clock frequency
    send_command(0x78)  # OLED command set disabled
    send_command(0x28)  # Function set (fundamental command set)
    send_command(0x01)  # Clear display
    time.sleep(0.2)
    send_command(0x0C)  # Display on (cursor and blink off)

def display_text():
    send_command(0x80)  # Set DDRAM address to 0 (line 1)
    for char in "Hello, OLED!":
        send_data(ord(char))

    send_command(0xC0)  # Set DDRAM address to 0x40 (line 2)
    for char in "No D/C Pin!":
        send_data(ord(char))

try:
    oled_init()
    display_text()
    print("Text displayed!")
except Exception as e:
    print(f"Error: {e}")
finally:
    spi.close()
    GPIO.cleanup()
