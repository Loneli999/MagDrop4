import qwiic_serlcd
import time

# Global variable to track initialization
lcd_initialized = False
lcd = None


def display(line1, line2):
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

        lcd.clearScreen()

        # Write the first line
        lcd.setCursor(0, 0)
        lcd.print(line1[:16])

        time.sleep(0.05)

        # Write the second line
        lcd.setCursor(0, 1)
        lcd.print(line2[:16])

    except Exception as e:
        print(f"An error occurred: {e}")
