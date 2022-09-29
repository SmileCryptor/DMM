import csv
from datetime import datetime
import sqlite3
from sqlite3 import Error
from collections import OrderedDict

class GenCSVKeepData:
    def __init__(self):
        print('')

    def writeData(self, data, filepath):
        data.insert(0, ['Recorded Time', 'Truck ID', 'Truck Weight', 'Measurement', 'B/L #'])

        # print(filepath)
        with open(filepath, 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(data)
        writeFile.close()

    def retriveData(self):
        data = []
        try:
            conn = sqlite3.connect('./res/db/weightrpi.db')
            sql = 'SELECT twi.DATETIME, twi.TRUCK_ID, twi.FB_WEIGHT, twi.UOM, twi.FB_ITEM_BARCODE FROM tbl_weight_info AS twi'
            cur = conn.cursor()
            cur.execute(sql)
            data = cur.fetchall()
            conn.commit()
        except Error as e:
            print(e)
            return
        finally:
            conn.close()
            return data

    def sortData(self, data):
        myDict = {}
        for item in data:
            myDict[item[0]] = item
        ordered = OrderedDict(sorted(myDict.items(), key = lambda t: t[0]))
        #print(ordered)
        data = []
        for key, val in ordered.items():
            data.append(val)
        #print(ordered.values())
        return data

    def doTask(self, path):
        #print('Truck:', truckid)
        self.writeData(self.sortData(self.retriveData()), path)

