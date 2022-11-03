from math import radians, cos, sin, asin, sqrt
from machine import UART
from micropyGPS import MicropyGPS
from machine import Pin
from time import sleep

total_distance1 = []
def distance(lat1, lat2, lon1, lon2):
     
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
      
    # calculate the result
    return(c * r)

def gps_main():
    uart = UART(2, baudrate=9600, bits=8, parity=None,
                stop=1, timeout=5000, rxbuf=1024)
    gps = MicropyGPS()
    global total_distance1
    while True:
        buf = uart.readline()
        if uart.any() == True:
            for char in buf:
    # Note the conversion to to chr, UART outputs ints normally
                gps.update(chr(char))
         
        #print('UTC Timestamp:', gps.timestamp)
        #print('Date:', gps.date_string('long'))
        #print('Satellites:', gps.satellites_in_use)
        print('Altitude:', gps.altitude)
        print('Latitude:', gps.latitude_string())
        print('Longitude:', gps.longitude_string())
        #print('Horizontal Dilution of Precision:', gps.hdop)     
        #print("gps speed", gps.speed_string())
        #print(gps.latitude_string()[0:7])
        print(gps.longitude_string())
        lon = float(gps.longitude_string()[0:3])  #stringslice her, alt efter plads 7 er skåret væk

        lat = float(gps.latitude_string()[0:3])
        if lat != 0.0 and lon != 0.0:
            
            #print(distance(lat1, lat2, lon1, lon2), "K.M")
            
            #total_distance3 = distance(lat1, lat2, lon1, lon2)
            #total_distance4 = total_distance3 + distance(lat1, lat2, lon1, lon2)
            lat_lon_tuple = (lat, lon)                                   
            total_distance1.append(lat_lon_tuple)
            #total_distance2 = sum(total_distance1)
            print("Total_distance1 listen",total_distance1)
            #print(total_distance4)
            
            #print(total_distance2, "Km")
            #print(total_distance1)
            length = len(total_distance1)
            print(length)
        else:
            print("No reading yet")


gps_main()
