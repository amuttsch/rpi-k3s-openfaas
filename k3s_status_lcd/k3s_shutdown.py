import lcd_i2c as lcd

lcd.lcd_init()
lcd.lcd_string('Good night!', lcd.LCD_LINE_1)
lcd.lcd_string('(-_-)zzz', lcd.LCD_LINE_2)

