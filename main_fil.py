import umqtt_robust2 as mqtt
from machine import Pin,ADC
from time import sleep
from machine import PWM
import neopixel


# Her kan i placere globale varibaler, og instanser af klasser
red_LED = Pin(25, Pin.OUT) # instans af Pin klassen AKA et Pin objekt

BUZZ_PIN = 22
buzzer = PWM(Pin(BUZZ_PIN, Pin.OUT), duty=0)
button = Pin(23, Pin.IN)

n = 12 #led antal i neopixel
p = 4  #pin led er forbundet til
np = neopixel.NeoPixel(Pin(p, Pin.OUT), n)
count = 0

analog_pin = ADC(Pin(34))
analog_pin.atten(ADC.ATTN_11DB)
analog_pin.width(ADC.WIDTH_12BIT)



while True:
    
    try:
        # Jeres kode skal starte her
        
        analog_val = analog_pin.read()
        #print("raw analog value: ", analog_val)
        volts = (analog_val * 0.00095238)*5
        battery_percentage = volts *100-320
        print("the battery precentage is:", battery_percentage,"%")
        mqtt.web_Print(battery_percentage)
        sleep(1)
        
        def set_color(r, g, b):
            for i in range(n):
                np[i] = (r, g, b)
                np.write()
        
        
        def clear():
            for i in range(n):
                np[i] = (0,0,0)
                np.write()
        
        def hex_to_rgb(value):
            value = value.lstrip("#")
            rgb_list = []
            lv = len(value)
            for i in range(0, lv, lv // 3):
                rgb_list.append(int(value[i:i + lv // 3], 16))
            return rgb_list        
        
        
       

        

        if mqtt.besked == "led_on":
            print("tænder led")
            red_LED.on()
            
        if mqtt.besked == "led_off":
            print("slukker led")
            red_LED.off()
                    
        if mqtt.besked == "svar_tilbage":
            mqtt.web_Print("ESP32 her!")
            
        if mqtt.besked == "spil a":
            print("spiller tone A")
            buzzer.duty(512)
            buzzer.freq(440)
            set_color(255, 0, 0)
            sleep(0.5)
            buzzer.duty(0)
            clear()
         
        if mqtt.besked == "spil b":
            print("spiller tone b")
            buzzer.duty(512)
            buzzer.freq(240)
            set_color(255, 255, 0)
            sleep(0.5)
            buzzer.duty(0)
            clear()
            
        if mqtt.besked == "spil c":
            print("spiller tone c")
            buzzer.duty(512)
            buzzer.freq(340)
            set_color(0, 0, 255)
            sleep(0.5)
            buzzer.duty(0)
            clear()
        
        if mqtt.besked == "go blue":
            set_color(0,0, 255)
        
        if mqtt.besked == "go red":
            set_color(255, 0, 0)
        
        if mqtt.besked == "go green":
            set_color(0, 255, 0)
        
        if mqtt.besked == "go off":
            clear()
        
        
        if "#" in mqtt.besked and len(mqtt.besked) == 7:
            try:
                rgb_list = hex_to_rgb(mqtt.besked)
                print(f"RGB list, {rgb_list}")
                set_color(int(rgb_list[0]), int(rgb_list[1]), int(rgb_list[2]))
            except:
                print("wrong hex value for neopixel ring")
        
       #---knap forsøg-----      
        first = button.value() #debounce
        sleep(0.01)
        second = button.value()  
        if first and not second:
            clear()
            #print(f"button pressed and count is {count}")
            count += 1
            if count == 1:
                np[0] = (255,0,0)
            elif count == 2:
                np[1] = (0,255,0)
            elif count == 3:
                np[2] = (0,0,255)
            elif count == 4:
                np[3] = (255,255,0)
            elif count == 5: 
                count = 0
        np.write()     
            
        # Jeres kode skal slutte her
        sleep(0.1)
        if len(mqtt.besked) != 0: # Her nulstilles indkommende beskeder
            mqtt.besked = ""            
        mqtt.syncWithAdafruitIO() # igangsæt at sende og modtage data med Adafruit IO             
        print(".", end = '') # printer et punktum til shell, uden et enter        
    # Stopper programmet når der trykkes Ctrl + c
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()