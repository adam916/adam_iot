import umqtt_robust2 as mqtt
from machine import Pin, ADC
from time import sleep
import neopixel
import time

analog_pin = ADC(Pin(34))
analog_pin.atten(ADC.ATTN_11DB)
analog_pin.width(ADC.WIDTH_12BIT)

n = 12
p = 15

np = neopixel.NeoPixel(Pin(p, Pin.OUT), n)

waitTime = 15
isWait=False
batteri_til_ada = 0
while isWait==True:
    newTime=time.time()
    if newTime-oldTime>waitTime:
        updateBP()
        isWait=False
        
    
def set_color(r, g, b):
    for i in range(n):
        np[i] = (r, g, b)
        np.write()
        
        
#This function is for the boot-up sequence. 
def batteryStart():
    for i in range (n):
        np[i]= (0, 100, 0)
        sleep(0.1)
    
        
#The main function of the battery. The battery percentage is calculated using the volt reading and multiplying by a specified amount determined by the number of batteries attached.
#In this case, 0.00100238 is used for the scenario in which two batteries are attached. If for a single battery, the number would be 0.00095238. 
def updateBP():
    global batteri_til_ada
    analog_val = analog_pin.read()
    volts = (analog_val * 0.00100238)*5
    battery_percentage = volts*100 - 320
    print("The battery percentage is:", battery_percentage, "%")
    print(volts)
    batteri_til_ada = battery_percentage
    #battery_percentage = 20 ///This value can be manually adjusted for testing purposes
        
    #These formulares are used for determining the amount of LED on the NEOPIXEL that needs to be lit. Since there are 12 lights, and battery percentage can go to 100%...
    #Its just a simple equation to determine the outcome.
    lightsOn=battery_percentage/8.33
    counter=lightsOn
    print(lightsOn)
    print(counter)
        
    #mqtt.web_print(battery_percentage)
        
    #This for loop lights all the correct LED's and is updated every 3.5 seconds. So even if the battery percentage might swing a bit, it will try to keep the correct amount lit at any time.
    for i in range (n):
        if counter >0:
            np[i] = (0,100,0)
            counter-=1
            print("Has lit a light")
            np.write()


    oldTime= time.time()
    isWait=True
    while isWait==True:
        
        if time.time() > oldTime + 55:
            print("has waiting")
            updateBP()
            isWait=False  
    
    #sleep(3.5)
    if len(mqtt.besked) != 0:
         mqtt.besked = ""
    mqtt.sync_with_adafruitIO()
    print(".", end = '')
    

def ada_bat():
    global batteri_til_ada
    print(batteri_til_ada)
    return batteri_til_ada
    


