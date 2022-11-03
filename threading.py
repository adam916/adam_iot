import _thread
from time import sleep
import tm1637  
from machine import Pin, I2C
import neopixel
from machine import UART
from micropyGPS import MicropyGPS
from imu import MPU6050  # https://github.com/micropython-IMU/micropython-mpu9x50

tm = tm1637.TM1637(clk=Pin(2), dio=Pin(4))

n = 12 #neopixel
p = 5 #pin

np = neopixel.NeoPixel(Pin(p, Pin.OUT), n)

i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)
imu = MPU6050(i2c)

def set_color(r, g, b):
    for i in range(n):
        np[i] = (r, g, b)
        np.write()

def gps_main():
    uart = UART(2, baudrate=9600, bits=8, parity=None,
                stop=1, timeout=5000, rxbuf=1024)
    gps = MicropyGPS()
    gps_1 = int(gps.satellites_in_use)
    while True:
        buf = uart.readline()
        for char in buf:
# Note the conversion to to chr, UART outputs ints normally
            gps.update(chr(char))
            
        print('UTC Timestamp:', gps.timestamp)
        print('Date:', gps.date_string('long'))
        print('Satellites:', gps.satellites_in_use)
        print('Altitude:', gps.altitude)
        print('Latitude:', gps.latitude_string())
        print('Longitude:', gps.longitude_string())
        print('Horizontal Dilution of Precision:', gps.hdop)
        
        if gps.satellites_in_use > 0:
            for i in gps_1(gps.satellites_in_use):
                np[i] = (200, 200, 200)
                np.write()
        sleep(3)

def IMU():
    acceleration = imu.accel
    gyroscope = imu.gyro  
    print ("Acceleration x: ", round(acceleration.x,2), " y:", round(acceleration.y,2),
           "z: ", round(acceleration.z,2))

    print ("gyroscope x: ", round(gyroscope.x,2), " y:", round(gyroscope.y,2),
           "z: ", round(gyroscope.z,2))

# data interpretation (accelerometer)

    if abs(acceleration.x) > 0.8:
        if (acceleration.x > 0):
            print("The x axis points upwards")
        else:
            print("The x axis points downwards")

    if abs(acceleration.y) > 0.8:
        if (acceleration.y > 0):
            print("The y axis points upwards")
        else:
            print("The y axis points downwards")

    if abs(acceleration.z) > 0.8:
        if (acceleration.z > 0):
            print("The z axis points upwards")
        else:
            print("The z axis points downwards")

# data interpretation (gyroscope)

    if abs(gyroscope.x) > 20:
        print("Rotation around the x axis")

    if abs(gyroscope.y) > 20:
        print("Rotation around the y axis")

    if abs(gyroscope.z) > 20:
        print("Rotation around the z axis")
    
    sleep(0.2)

def dis():
    tm.show("1111")
    print("1111")

#_thread.start_new_thread(dis, ())
#sleep(5)

"""def func():
    print("Ran")
    sleep(2)
    print("Done")

#x = _thread(target=func)
#_thread.start_new_thread(func, ())
#sleep(5)

def func_2():
    print("Runnning")
    sleep(2)
    print("Done done")"""

#y = _thread(target=func_2)


_thread.start_new_thread(dis, ())
#_thread.start_new_thread(func, ())
#_thread.start_new_thread(func_2, ())
#_thread.start_new_thread(gps_main, ())
_thread.start_new_thread(set_color, (100, 0, 0))
sleep(2)
_thread.start_new_thread(set_color, (0, 100, 0))
sleep(2)
_thread.start_new_thread(set_color, (0, 0, 100))
sleep(2)
_thread.start_new_thread(set_color, (0, 0, 0))

sleep(5)
tm.show("2222")
print("Faerdig funktion")
sleep(5)