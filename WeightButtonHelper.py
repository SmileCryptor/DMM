from WeightReadingHX711Thread import WeightReadingHX711Thread
import sqlite3
from sqlite3 import Error
from WeightReadingRS232Thread import WeightReadingRs232Thread

class WeightButtonHelper:
    def __init__(self, GUI):
        self.GUI = GUI

    def readHX711(self):
        WeightReadingHX711Thread(self.GUI).start()

    def readRS232(self):
        WeightReadingRs232Thread(self.GUI).start()

    def insertData(self, data):
        stat = False
        try:
            conn = sqlite3.connect('./res/db/weightrpi.db')
            sql = 'INSERT INTO tbl_weight_info(truckid,weight,measurement,barcode, scantype,recorded) VALUES (?,?,?,?,?,?)'
            cur = conn.cursor()
            cur.execute(sql, data)
            conn.commit()
            stat = True
        except Error as e:
            print(e)
            stat = False
        finally:
            conn.close()

        try:
            conn = sqlite3.connect('./res/db/weightfiverpi.db')
            sql = 'INSERT INTO tbl_weight_five_info(truckid,weight,measurement,barcode, scantype,recorded) VALUES (?,?,?,?,?,?)'
            cur = conn.cursor()
            cur.execute(sql, data)
            conn.commit()
            stat = True
        except Error as e:
            print(e)
            stat = False
        finally:
            conn.close()

        print('Data Stored')
        return stat


