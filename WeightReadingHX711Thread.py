import threading
import sqlite3
import re
import time
import decimal
from barcode.writer import ImageWriter
import barcode
from sqlite3 import Error
from datetime import datetime
from SerialConfig import SerialConfig
import qrcode
from PIL import Image
import numpy as np
import random
from HX711Serial import HX711Serial
from Config import _App

class WeightReadingHX711Thread(threading.Thread):
    def __init__(self, GUI):
        threading.Thread.__init__(self)
        self.GUI = GUI
        self.OLDWEIGHT = '0'

    def decodeSerialRes(self, res):
        try:
            print("read data: " + res)
            response = re.sub(r"[^a-zA-Z0-9]+", ' ', res)
            response = response.strip()
        except:
            response = ''
        finally:
            return response

    def initSerial(self):
        self.rs232 = HX711Serial()
        stat = self.rs232.checkSerialConfig()
        self.rsserial = self.rs232.Hx711
        return stat

    def run(self):
        print('Entering Into HX711 Thread')
        while _App.HX711STAT:
            if _App.DEBUG is True:
                ############ TESTING
                cval = random.randint(0, 1)
                rval = random.randint(5000, 10000) * 1.7
                if cval == 0:
                    response = str(rval) + ' LBS GR'
                else:
                    response = str(rval) + ' KG GR'
                weight = self.extractDigit(response)
                if weight != '-1':
                    self.doProcessing(weight)
                # time.sleep(self.window.INTERVAL)
                time.sleep(1)
            else:
                if self.initSerial():
                    try:
                        response = self.rsserial.get_weight_mean(10)
                        if response is not None:
                            currentWeight = (float)(response)
                            currentWeight = currentWeight / 1.0
                            currentWeight = round(currentWeight)
                            if self.rs232.ROUNDOFF > 2:
                                currentWeight = currentWeight + (self.rs232.ROUNDOFF - 1)
                            print('Measured...', currentWeight)
                            self.doProcessing(str(currentWeight))
                        time.sleep(self.rs232.INTERVAL)
                    except Exception as e:
                        print('HX711 Serial Read Error:', e)
                        time.sleep(0.1)
                else:
                    break
        print('Exiting From HX711 Thread')

    def extractDigit(self, response):
        try:
            value = (float)(re.findall(r"[-+]?\d*\.\d+|\d+", response)[0])
            # print(response)
            value = "{0:.4f}".format(value)
            value = self.dropzeros(value)
        except:
            value = -1
            print('Weight conversion error')
        finally:
            return str(value)

    def dropzeros(self, number):
        mynum = decimal.Decimal(number).normalize()
        return mynum.__trunc__() if not mynum % 1 else float(mynum)

    def weightConversion(self, weight):
        if self.GUI.WEIGHTMODE == 'KG':
            weight = float(weight) * 2.20462
            weight = round(weight,1)
            weight = str(weight)
        return weight

    def doProcessing(self, weight):
        try:
            weight = self.weightConversion(weight)
            if weight != self.OLDWEIGHT:
                self.OLDWEIGHT = weight
                EAN = barcode.get_barcode_class('code128')
                ean = EAN(weight, writer=ImageWriter())
                fullname = ean.save('./res/img/barcode')

                if self.GUI.WEIGHTMODE == 'KG':
                    fimg = Image.open("./res/img/kg.jpg")
                else:
                    fimg = Image.open("./res/img/lbs.jpg")
                bar = Image.open("./res/img/barcode.png")
                basewidth, height = bar.size
                # wpercent = (basewidth / float(fimg.size[0]))
                # hsize = int((float(fimg.size[1]) * float(wpercent)))
                fimg = fimg.resize((basewidth, 55), Image.ANTIALIAS)
                img_merge = np.vstack((np.asarray(bar), np.asarray(fimg)))
                img_merge = Image.fromarray(img_merge)
                barimg = img_merge.resize((240, 160), Image.ANTIALIAS)
                #img.save('./res/img/barcode_resized.jpg')

                qr = qrcode.QRCode(version=1,
                                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                                    box_size=50,
                                    border=1,)
                qr.add_data(weight+' '+self.GUI.WEIGHTMODE)
                qr.make(fit=True)
                qrimg = qr.make_image(fill_color="black", back_color="white")
                #age.open("./res/img/qrcode.png")
                qrimg = qrimg.resize((160, 160), Image.ANTIALIAS)
                #qrimg.save('./res/img/qrcode_resized.jpg')

                self.GUI.CURRENTWEIGHT = weight
                self.GUI.updateWeightText(weight)
                self.GUI.updateBarCodeImage(barimg)
                self.GUI.updateQrCodeImage(qrimg)

        except:
            print('Data Processing Error')