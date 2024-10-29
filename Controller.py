import pyfirmata2
import atexit
import time


comport = '/dev/cu.usbmodem1401'
board = pyfirmata2.Arduino(comport)

led_1 = board.get_pin("d:13:o")

# Define LCD pins
lcd_rs = board.get_pin("d:12:o")  # RS pin
lcd_en = board.get_pin("d:11:o")  # Enable pin
lcd_d4 = board.get_pin("d:5:o")   # Data pin 4
lcd_d5 = board.get_pin("d:4:o")   # Data pin 5
lcd_d6 = board.get_pin("d:3:o")   # Data pin 6
lcd_d7 = board.get_pin("d:2:o")   # Data pin 7

# Define LCD dimensions
lcd_columns = 16
lcd_rows = 2

# Initialize LCD
def lcd_init():
    lcd_write(0x33, LCD_CMD)
    lcd_write(0x32, LCD_CMD)
    lcd_write(0x06, LCD_CMD)
    lcd_write(0x0C, LCD_CMD)
    lcd_write(0x28, LCD_CMD)

# Write data to LCD
def lcd_write(bits, mode):
    lcd_rs.write(mode)
    lcd_d4.write(bits & 0x10 == 0x10)
    lcd_d5.write(bits & 0x20 == 0x20)
    lcd_d6.write(bits & 0x40 == 0x40)
    lcd_d7.write(bits & 0x80 == 0x80)
    lcd_toggle_enable()
    lcd_d4.write(bits & 0x01 == 0x01)
    lcd_d5.write(bits & 0x02 == 0x02)
    lcd_d6.write(bits & 0x04 == 0x04)
    lcd_d7.write(bits & 0x08 == 0x08)
    lcd_toggle_enable()

# Toggle Enable pin
def lcd_toggle_enable():
    lcd_en.write(True)
    time.sleep(0.000001)
    lcd_en.write(False)
    time.sleep(0.000001)

# Clear LCD
def lcd_clear():
    lcd_write(0x01, LCD_CMD)
    time.sleep(0.002)

# Set cursor position
def lcd_set_cursor(col, row):
    col = max(0, min(col, lcd_columns - 1))
    row = max(0, min(row, lcd_rows - 1))
    offsets = [0x00, 0x40, 0x14, 0x54]
    lcd_write(0x80 | (col + offsets[row]), LCD_CMD)

# Write text to LCD
def lcd_write_string(message):
    for char in message:
        lcd_write(ord(char), LCD_CHR)

# LCD commands
LCD_CHR = True
LCD_CMD = False

# Initialize LCD
lcd_init()
lcd_clear()

def led(ClassIndex):
    if len(ClassIndex) == 0:
        led_1.write(0)
        lcd_clear()  # Clear LCD if no faces detected
    else:
        led_1.write(1)
        lcd_write_string("Person detected")  # Display message on LCD

def led_off():
    led_1.write(0)
    lcd_clear()  # Clear LCD when LED is turned off

def cleanup():
    led_off()
    board.exit()

atexit.register(cleanup)
