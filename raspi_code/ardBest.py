import serial
import RPi.GPIO as GPIO
import time



# Define GPIO to LCD mapping
LCD_RS = 26
LCD_E  = 19
LCD_D4 = 13 
LCD_D5 = 6
LCD_D6 = 5
LCD_D7 = 11
LED_ON = 15

RELAY_IN1 = 17
RELAY_IN2 = 27
RELAY_IN3 = 22
RELAY_IN4 = 23

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line 

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005




def main():

    # variables to control state changes
    lcdLdrA = False
    lcdLdrB = False
    lcdHumA = False
    lcdHumB = False
    lcdHumC = False
    lcdHumD = False
    ldrA = 0
    ldrB = 0
    lineA = ""
    lineB = ""
    clean_lcd_count = 0


    try:

        # Initialise display
        lcd_init()
        relay_init()

        serA = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
        serB = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        serA.flush()
        serB.flush()

        

        while True:

            # ARDUINO A ====================================================
            if serA.in_waiting > 0: 

                lineA = serA.readline().decode('utf-8').rstrip()
                print("line A = " + lineA)

                if lineA[:3] == "ldr":
                    ldrA, lcdLdrA, clean_lcd_count = ldrAbehaviour(lineA, lcdLdrA, clean_lcd_count)

                    # Communications
                    if ldrA == 0:
                        serA.write(b"dark\n")
                    elif ldrA == 1:
                        serA.write(b"light\n")
                
                elif lineA[:4] == "huma":
                    lcdHumA, clean_lcd_count = humAbehaviour(lineA, lcdHumA, clean_lcd_count)
                elif lineA[:4] == "humb":
                    lcdHumB, clean_lcd_count = humBbehaviour(lineA, lcdHumB, clean_lcd_count)
            
            # ARDUINO B ====================================================
            if serB.in_waiting > 0: 

                lineB = serB.readline().decode('utf-8').rstrip()
                print("line B = " + lineB)

                if lineB[:3] == "ldr":
                    ldrB, lcdLdrB, clean_lcd_count = ldrBbehaviour(lineB, lcdLdrB, clean_lcd_count)

                    # Communications
                    if ldrB == 0:
                        serB.write(b"dark\n")
                    elif ldrB == 1:
                        serB.write(b"light\n")
                
                elif lineB[:4] == "huma":
                    lcdHumC,clean_lcd_count = humCbehaviour(lineB, lcdHumC, clean_lcd_count)
                elif lineB[:4] == "humb":
                    lcdHumD,clean_lcd_count = humDbehaviour(lineB, lcdHumD, clean_lcd_count)


            # Controls duration of LCD ======================================
            clean_lcd_count += 1
            
            if clean_lcd_count >= 200000:
                
                lcd_byte(LCD_LINE_1, LCD_CMD)
                lcd_string("",2)
                lcd_byte(LCD_LINE_2, LCD_CMD)
                lcd_string("",2)

                clean_lcd_count = 0

    finally: # If interrupted, close GPIO and turn off LCD

        lcd_byte(LCD_LINE_1, LCD_CMD)
        lcd_string("",2)
        lcd_byte(LCD_LINE_2, LCD_CMD)
        lcd_string("",2)	
        GPIO.cleanup()


def ldrAbehaviour(lineA, lcdLdrA, clean_lcd_count):
  
    stringA = lineA[3:]
					  
    if float(stringA) >= 500:
        
        if lcdLdrA == False:
            
            lcdLdrA = True

            clean_lcd_count = 0 # reset clean
        
            lcd_byte(LCD_LINE_1, LCD_CMD)
            lcd_string("Turning on",2)
            lcd_byte(LCD_LINE_2, LCD_CMD)
            lcd_string("LED A",2)

        return 0, lcdLdrA, clean_lcd_count; 

    else:
        
        if lcdLdrA:
            
            lcdLdrA = False
        
            clean_lcd_count = 0 # reset clean  

            lcd_byte(LCD_LINE_1, LCD_CMD)
            lcd_string("Turning off",2)
            lcd_byte(LCD_LINE_2, LCD_CMD)
            lcd_string("LED A",2)
        
        return 1, lcdLdrA, clean_lcd_count;


def ldrBbehaviour(lineB, lcdLdrB, clean_lcd_count):
  
    stringB = lineB[3:]
					  
    if float(stringB) >= 500:
        
        if lcdLdrB == False:
            
            lcdLdrB = True
            clean_lcd_count = 0 # reset clean
        
            lcd_byte(LCD_LINE_1, LCD_CMD)
            lcd_string("Turning on",2)
            lcd_byte(LCD_LINE_2, LCD_CMD)
            lcd_string("LED B",2)

        return 0, lcdLdrB, clean_lcd_count; 

    else:
        
        if lcdLdrB:
            
            lcdLdrB = False 
            clean_lcd_count = 0 # reset clean  

            lcd_byte(LCD_LINE_1, LCD_CMD)
            lcd_string("Turning off",2)
            lcd_byte(LCD_LINE_2, LCD_CMD)
            lcd_string("LED B",2)
            
        return 1, lcdLdrB, clean_lcd_count;
  
def humAbehaviour(lineA, lcdHumA, clean_lcd_count):

    stringA = lineA[4:]
					  
    if float(stringA) <= 500:
        
        GPIO.output(RELAY_IN1, True)
        
        if lcdHumA == False:
            
            lcdHumA = True
            clean_lcd_count = 0 # reset clean
        
            lcd_byte(LCD_LINE_1, LCD_CMD)
            lcd_string("Turning off",2)
            lcd_byte(LCD_LINE_2, LCD_CMD)
            lcd_string("PUMP A",2) 
           
    else:
        
        GPIO.output(RELAY_IN1, False)
        
        if lcdHumA:
            
            lcdHumA = False
            clean_lcd_count = 0 # reset clean  

            lcd_byte(LCD_LINE_1, LCD_CMD)
            lcd_string("Turning on",2)
            lcd_byte(LCD_LINE_2, LCD_CMD)
            lcd_string("PUMP A",2)
            
    return lcdHumA, clean_lcd_count
    
def humBbehaviour(lineA, lcdHumB, clean_lcd_count):

    stringA = lineA[4:]
					  
    if float(stringA) <= 500:
        
        GPIO.output(RELAY_IN2, True)
        
        if lcdHumB == False:
            
            lcdHumB = True
            clean_lcd_count = 0 # reset clean
        
            lcd_byte(LCD_LINE_1, LCD_CMD)
            lcd_string("Turning off",2)
            lcd_byte(LCD_LINE_2, LCD_CMD)
            lcd_string("PUMP B",2) 
           
    else:
        
        GPIO.output(RELAY_IN2, False)
        
        if lcdHumB:
            
            lcdHumB = False     
            clean_lcd_count = 0 # reset clean  

            lcd_byte(LCD_LINE_1, LCD_CMD)
            lcd_string("Turning on",2)
            lcd_byte(LCD_LINE_2, LCD_CMD)
            lcd_string("PUMP B",2)
        
    return lcdHumB, clean_lcd_count

def humCbehaviour(lineB, lcdHumC, clean_lcd_count):

    stringB = lineB[4:]
					  
    if float(stringB) <= 500:
        
        GPIO.output(RELAY_IN3, True)
        
        if lcdHumC == False:
            
            lcdHumC = True
            clean_lcd_count = 0 # reset clean
        
            lcd_byte(LCD_LINE_1, LCD_CMD)
            lcd_string("Turning off",2)
            lcd_byte(LCD_LINE_2, LCD_CMD)
            lcd_string("PUMP C",2) 
            
    else:
        
        GPIO.output(RELAY_IN3, False)
        
        if lcdHumC:
            
            lcdHumC = False
            clean_lcd_count = 0 # reset clean  

            lcd_byte(LCD_LINE_1, LCD_CMD)
            lcd_string("Turning on",2)
            lcd_byte(LCD_LINE_2, LCD_CMD)
            lcd_string("PUMP C",2)
        
    return lcdHumC, clean_lcd_count
    
def humDbehaviour(lineB, lcdHumD, clean_lcd_count):

    stringB = lineB[4:]
					  
    if float(stringB) <= 500:
        
        GPIO.output(RELAY_IN4, True)
        
        if lcdHumD == False:
            
            lcdHumD = True
            clean_lcd_count = 0 # reset clean
        
            lcd_byte(LCD_LINE_1, LCD_CMD)
            lcd_string("Turning off",2)
            lcd_byte(LCD_LINE_2, LCD_CMD)
            lcd_string("PUMP D",2) 
           
    else:
        
        GPIO.output(RELAY_IN4, False)
        
        if lcdHumD:
            
            lcdHumD = False
            clean_lcd_count = 0 # reset clean  

            lcd_byte(LCD_LINE_1, LCD_CMD)
            lcd_string("Turning on",2)
            lcd_byte(LCD_LINE_2, LCD_CMD)
            lcd_string("PUMP D",2)
        
    return lcdHumD, clean_lcd_count

def relay_init():
    GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
    GPIO.setup(RELAY_IN1, GPIO.OUT)
    GPIO.setup(RELAY_IN2, GPIO.OUT)
    GPIO.setup(RELAY_IN3, GPIO.OUT)
    GPIO.setup(RELAY_IN4, GPIO.OUT)

def lcd_init():
    GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
    GPIO.setup(LCD_E, GPIO.OUT)  # E
    GPIO.setup(LCD_RS, GPIO.OUT) # RS
    GPIO.setup(LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(LCD_D5, GPIO.OUT) # DB5
    GPIO.setup(LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(LCD_D7, GPIO.OUT) # DB7
    GPIO.setup(LED_ON, GPIO.OUT) # Backlight enable  
    # Initialise display
    lcd_byte(0x33,LCD_CMD)
    lcd_byte(0x32,LCD_CMD)
    lcd_byte(0x28,LCD_CMD)
    lcd_byte(0x0C,LCD_CMD)  
    lcd_byte(0x06,LCD_CMD)
    lcd_byte(0x01,LCD_CMD)  

def lcd_string(message,style):
    # Send string to display
    # style=1 Left justified
    # style=2 Centred
    # style=3 Right justified

    if style==1:
        message = message.ljust(LCD_WIDTH," ")  
    elif style==2:
        message = message.center(LCD_WIDTH," ")
    elif style==3:
        message = message.rjust(LCD_WIDTH," ")

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)

def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command

    GPIO.output(LCD_RS, mode) # RS

    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x10==0x10:
        GPIO.output(LCD_D4, True)
    if bits&0x20==0x20:
        GPIO.output(LCD_D5, True)
    if bits&0x40==0x40:
        GPIO.output(LCD_D6, True)
    if bits&0x80==0x80:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    time.sleep(E_DELAY)    
    GPIO.output(LCD_E, True)  
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)  
    time.sleep(E_DELAY)      

    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x01==0x01:
        GPIO.output(LCD_D4, True)
    if bits&0x02==0x02:
        GPIO.output(LCD_D5, True)
    if bits&0x04==0x04:
        GPIO.output(LCD_D6, True)
    if bits&0x08==0x08:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    time.sleep(E_DELAY)    
    GPIO.output(LCD_E, True)  
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)  
    time.sleep(E_DELAY)   

if __name__ == '__main__':
    main()




