
import compression
import monitor
import time
import os 
import configparser
import datetime
import rpi
import serial
output = monitor.Monitor()

config = configparser.ConfigParser()
config.read("settings.ini")
enable_compression = config.getboolean("DATA", "Compression")
sample_second = config.getfloat("DATA", "SamplingSeconds")
refresh_rate = config.getfloat("DATA", "RefreshRate")

output.print("Compression: " + enable_compression)

time.sleep(0.5)
output.clear()


exporter = compression.Csv_Export()

start_time = time.time()
rpi = rpi.RPi()
ser = serial.Serial('/dev/ttyS0', 9600)
output.clear()
output.print("WAIT TILL INIT")
time.sleep(1)
output.clear()
output.print("OK!")
time.sleep(0.5)
while True:

    print(rpi.get_cpu_temp())
        
    refresh_start = time.time()

    while time.time() - refresh_start < refresh_rate:  f

        output.clear()
        data = ser.readline().decode('utf-8').strip()
        if data:
            output.print(f"{data}")

        time.sleep(refresh_rate)   

    clock_time = time.time() - start_time
    
    if clock_time >= sample_second:
        start_time = time.time()   
        print(f"[{datetime.date.today()}]: CSV produced.")
        exporter.csv_export(current, voltage, enable_compression)
