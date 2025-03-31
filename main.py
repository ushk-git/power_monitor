import acs712
import compression
import monitor
import time
import os 
import configparser
import datetime
import rpi
output = monitor.Monitor()

config = configparser.ConfigParser()
config.read("settings.ini")
enable_compression = config.getboolean("DATA", "Compression")
sample_second = config.getfloat("DATA", "SamplingSeconds")
refresh_rate = config.getfloat("DATA", "RefreshRate")

output.print("Compression")
output.print(enable_compression)
time.sleep(0.5)
output.clear()

acs712 = acs712.Acs712()
exporter = compression.Csv_Export()

start_time = time.time()
rpi = rpi.RPi()

while True:

    print(rpi.get_cpu_temp())
        
    refresh_start = time.time()

    while time.time() - refresh_start < refresh_rate:  
        current = acs712.get_current()
        voltage = acs712.get_voltage()
        power = current * voltage

        output.clear()
        output.print(f"CUR: {current:.2f} A  VOLT: {voltage:.2f} V")
        output.print(f"POWER: {power:.2f} W")
        time.sleep(0.1)   
    print
    clock_time = time.time() - start_time
    
    if clock_time >= sample_second:
        start_time = time.time()   
        print(f"[{datetime.date.today()}]: CSV produced.")
        exporter.csv_export(current, voltage, enable_compression)
