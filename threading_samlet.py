#from imu_func import IMU_func
from gps_funktion import gps_main
#from filnavn import start
#from filnavn import
import _thread

while True:
    _thread.start_new_thread(gps_main, ())
    #_thread.start_new_thread(IMU_func, ()) både Display og IMU
    # Anden IMU-funktion med hastighed
    # Neopixel-funktion