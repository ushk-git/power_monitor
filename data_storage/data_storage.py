import datetime
import csv
import zlib
import os
import glob
import time



compress = True

class ZLib_Helper:
    def compress(self, file):
        with open(file, 'rb') as fi:
            file_data = fi.read()
        file_compress = zlib.compress(file_data)
        compressed_file_name = file + "-compressed.zlib"
        with open(compressed_file_name, 'wb') as fi:
            fi.write(file_compress)

    def decompress(self, file):
        with open(file, 'rb') as fi:
            file_data = fi.read()
        file_decompress = zlib.decompress(file_data)
        decompressed_file_name = file.removesuffix("-compressed.zlib")
        with open(decompressed_file_name, 'wb') as fi:
            fi.write(file_decompress)


curr_date = datetime.date.today()

class Csv_Export:
    def __init__(self):
        self.rows = []
        return

    def csv_export(self, current, voltage):
        global curr_date
        if curr_date != datetime.date.today():
            curr_date = datetime.date.today()

        file_name = str(curr_date) + '_PowerData.csv'
        row = {'time': datetime.datetime.now().time(), 'power': current * voltage, 'current': current, 'voltage': voltage}
        self.rows.append(row)

        with open(file_name, 'w', newline='\n') as csvfile:
            fieldnames = ['time', 'power', 'current', 'voltage']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.rows)

        if compress:
            cd = ZLib_Helper()
            cd.compress(file_name)
            os.remove(file_name)
