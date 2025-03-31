import os
import smbus2
import time

BACKLIGHT = 0x08  
I2C_ADDR = 0x27
ENABLE = 0b00000100 
LCD_CHR = 1
LCD_CMD = 0
LCD_LINE_1 = 0x80  
LCD_LINE_2 = 0xC0 
LCD_WIDTH = 16  

bus = smbus2.SMBus(1)

class Monitor:
    def __init__(self):
        self.lcd_send_byte(0x33, LCD_CMD)
        self.lcd_send_byte(0x32, LCD_CMD)
        self.lcd_send_byte(0x06, LCD_CMD)
        self.lcd_send_byte(0x0C, LCD_CMD)
        self.lcd_send_byte(0x28, LCD_CMD)
        self.lcd_send_byte(0x01, LCD_CMD)
        time.sleep(0.0005)
        bus.write_byte(I2C_ADDR, BACKLIGHT)

    def lcd_send_byte(self, bits, mode):
        high_bits = mode | (bits & 0xF0) | ENABLE | BACKLIGHT
        low_bits = mode | ((bits << 4) & 0xF0) | ENABLE | BACKLIGHT
        bus.write_byte(I2C_ADDR, high_bits)
        time.sleep(0.0005)
        bus.write_byte(I2C_ADDR, high_bits & ~ENABLE)
        time.sleep(0.0005)
        bus.write_byte(I2C_ADDR, low_bits)
        time.sleep(0.0005)
        bus.write_byte(I2C_ADDR, low_bits & ~ENABLE)    
    
    def print(self, text):
    	text = str(text)
    
    # Ensure the text is not longer than twice the LCD width (16 chars per line, so 32 chars max)
    	text = text[:LCD_WIDTH * 2]
    
    # Split text into two parts, one for each line
    	line_1 = text[:LCD_WIDTH]
    	line_2 = text[LCD_WIDTH:]

    # Print first line
    	self.lcd_send_byte(LCD_LINE_1, LCD_CMD)
    	for char in line_1:
        	self.lcd_send_byte(ord(char), LCD_CHR)

    # Print second line
    	self.lcd_send_byte(LCD_LINE_2, LCD_CMD)
    	for char in line_2:
        	self.lcd_send_byte(ord(char), LCD_CHR)
   
    def clear(self):
        self.lcd_send_byte(0x01, LCD_CMD)
        time.sleep(0.002)
