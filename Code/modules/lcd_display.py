import qwiic_serlcd
import time

# Global variable to track initialization
lcd_initialized = False
lcd = None  # Declare LCD object globally


def display(line1, line2):
    """
    Clears the LCD screen and displays two lines of text.
    Initializes the LCD and backlight only on the first call.

    Parameters:
        line1 (str): Text for the first line.
        line2 (str): Text for the second line.
    """
    global lcd, lcd_initialized

    try:
        # Initialize LCD and backlight only once
        if not lcd_initialized:
            lcd = qwiic_serlcd.QwiicSerlcd()
            if not lcd.connected:
                print("LCD not detected. Check connections.")
                return

            # Initialize the backlight
            lcd.setBacklight(0, 0, 255)  # RGB for blue
            lcd_initialized = True
            lcd.noAutoscroll()
            print("LCD initialized.")

        # Clear the screen
        lcd.clearScreen()

        # Write the first line
        lcd.setCursor(0, 0)  # Move to the first row
        lcd.print(line1[:16])  # Truncate text to 16 characters if needed

        time.sleep(0.05)

        # Write the second line
        lcd.setCursor(0, 1)  # Move to the second row
        lcd.print(line2[:16])  # Truncate text to 16 characters if needed

    except Exception as e:
        print(f"An error occurred: {e}")
