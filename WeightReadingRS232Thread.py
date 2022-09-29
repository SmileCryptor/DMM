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
from PIL.ImageQt import ImageQt
import numpy as np
import random
import io

from PyQt5.QtGui import QPixmap, QImage

from RS232Serial import RS232Serial
from Config import _App
from Config import APP_STATE

class WeightReadingRs232Thread(threading.Thread):
    def __init__(self, GUI):
        threading.Thread.__init__(self)
        self.GUI = GUI
        self.OLDWEIGHT = '0'
        self.TEMPWEIGHT = '0'
        self.WCOUNT = 0
        self.WSTAT = False

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
        self.rs232 = RS232Serial()
        stat = self.rs232.checkSerial()
        self.rsserial = self.rs232.ser
        return stat

    def run(self):
        print('Entering Into RS232 Thread')
        
        if _App.DEBUG is False and not self.initSerial():
            return

        while _App.RS232STAT:
            if _App.DEBUG_OUTPUT:
                print('RS232 Thread: running...')

            if _App.LOG_TO_FILE:
                _App.append_to_log('RS232 Thread: running...')

            if _App.APPSTATE.value < APP_STATE.STATE_BEGIN_LIFT.value:
                self.OLDWEIGHT = '0'
                self.TEMPWEIGHT = '0'
                self.WSTAT = False
                time.sleep(1)
                continue

            if _App.DEBUG is True:
                ############ TESTING
                cval = random.randint(0, 1)
                mval = random.randint(0, 1)
                rval = random.randint(5000, 10000) * 1.7

                if cval == 0:
                    response = str(rval) + ' LBS GR'
                else:
                    response = str(rval) + ' KG GR'

                if mval == 1:
                    response += ' M'

                print("received data: " + response)
                weight = self.extractDigit(response)
                if weight != '-1':
                    self.doProcessing(response, weight)
                # time.sleep(self.window.INTERVAL)
                time.sleep(5)
            else:
                if self.rsserial.isOpen():
                    self.rsserial.flushInput()
                    self.rsserial.flushOutput()
                    #time.sleep(0.5)
                try:
                    if self.rsserial.isOpen():
                        response = self.rsserial.readline()
                        print("Pure Response:" + response)

                        if len(response) > 5:
                            response = self.rsserial.readline().decode('UTF-8')
                            # response = self.rsserial.readline().decode('UTF-8')
                            print("read data: " + response)
                            response_ravas = response
                            #response_ravas = re.sub(r"[^a-zA-Z]+", ' ', response)
                            response_ravas = response_ravas.strip()
                            print("responseravas" + response_ravas)
                            response = re.sub(r"[^a-zA-Z0-9]+", ' ', response)
                            response = response.strip()
                            print("response" + response)

                            if _App.DEBUG_OUTPUT:
                                print("received data: " + response)

                            if _App.LOG_TO_FILE:
                                _App.append_to_log("received data: {}".format(response))

                            if _App._Settings.PARSERMODE == 'AVERY':
                                if response.startswith('SP') != True:
                                    self.doProcessing('EEEEE', '-1')
                                    return

                            if _App._Settings.PARSERMODE == 'DF1500':
                                if response.startswith('SP') == True:
                                    self.doProcessing('EEEEE', '-1')
                                    return

                            if _App._Settings.PARSERMODE == 'RAVAS':
                                print("ravas:" + response_ravas)
                                if response_ravas.startswith('--') == True :
                                    print("ravas" + response_ravas)
                                    self.doProcessing('EEEEE', '-2')

                            if len(response) >= 0:
                                currentWeight = self.extractDigit(response)
                                if currentWeight != '-1':
                                    self.doProcessing(response, currentWeight)
                                else:
                                    print('Weight coming Zero')

                        elif _App._Settings.PARSERMODE == 'RAVAS':
                            self.doProcessing(response, '-1')
                        time.sleep(self.rs232.INTERVAL)
                        print('streaming stop')
                        #self.rsserial.flushInput()
                        #self.rsserial.flushOutput()

                except Exception as e:
                    print('RS232 Serial Read Error:', e)
                    time.sleep(0.1)

        print('Exiting From RS232 Thread')

    def extractDigit(self, response):
        try:
            value = (float)(re.findall(r"[-+]?\d*\.\d+|\d+", response)[0])
            # print(response)
            #value = "{0:.4f}".format(value)
            value = int(value)
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
        if _App._Settings.WEIGHTMODE == 'KG':
            weight = float(weight) * 2.20462
            weight = round(weight, 1)
            weight = str(weight)
        return weight

    def doProcessing(self, response, weight):
        #weight = self.weightConversion(weight)
        try:
            
            if weight == '-1':
                self.GUI.newLiftSet(weight, '', None, None)
                self.OLDWEIGHT = '-1'
                return

            if weight == '-2':
                self.GUI.newLiftSet(weight, '', None, None)
                self.OLDWEIGHT = '-2'
                return
            
            if 'M' not in response:
                if _App.DEBUG is True:
                    if float(weight) < _App._Settings.WEIGHTTHRESHOLD:
                        #self.GUI.updateWeightText("NO LOAD", "")
                        #self.GUI.updateNoneCodeImage()
                        #self.GUI.setNewLift(0, "")
                        self.GUI.newLiftSet("", "", None, None)
                        #_App.APPSTATE = APP_STATE.STATE_BEGIN_LIFT
                        #self.GUI.changeAppState()
                        return

                    self.OLDWEIGHT = weight

                    weightmode = ''

                    if 'KG' in response:
                        weightmode = 'KGS'
                    elif 'LB' in response:
                        weightmode = 'LBS'
                    elif response.endswith('L'):
                        weightmode = 'LBS'
                    elif response.endswith('K'):
                        weightmode = 'KGS'

                    #_App._Settings.WEIGHTMODE = weightmode
                    weight_code = weight + ' ' + weightmode
                    print("weight: ", weight_code)

                    EAN = barcode.get_barcode_class('code128')
                    ean = EAN(weight_code, writer = ImageWriter())
                    bar = ean.render()
                    barimg = bar.resize((240, 160), Image.ANTIALIAS)
                    pix_bar = QPixmap.fromImage(self.convert_barimg(barimg))

                    qr = qrcode.QRCode(version = 1,
                                        error_correction = qrcode.constants.ERROR_CORRECT_L,
                                        box_size = 7,
                                        border = 1,)
                    qr.add_data(weight_code)
                    qr.make(fit = True)
                    qrimg = qr.make_image(fill_color = "black", back_color = "white")
                    pix_qr = QPixmap.fromImage(self.convert_qrimg(qrimg))

                    #self.GUI.setNewLift(float(weight), weightmode)
                    self.GUI.newLiftSet(weight, weightmode, pix_bar, pix_qr)
                    return

                if weight != self.OLDWEIGHT and self.WSTAT == False:
                    self.WCOUNT = 0
                    self.TEMPWEIGHT = weight
                    self.WSTAT = True
                elif weight != self.TEMPWEIGHT and self.WSTAT == True:
                    if weight == self.OLDWEIGHT:
                        self.WCOUNT = 0
                        self.TEMPWEIGHT = '0'
                        self.WSTAT = False
                    else:
                        self.WCOUNT = 0
                        self.TEMPWEIGHT = weight
                        self.WSTAT = True
                elif weight == self.TEMPWEIGHT:
                    if ( ( int(weight) == 0 and self.WCOUNT >= _App.WEIGHT_TRY_ZERO ) or ( int(weight) > 0 and self.WCOUNT >= _App.WEIGHT_TRY_NONZERO ) ) and self.WSTAT == True:
                        self.WSTAT = False
                        self.WCOUNT = 0

                        if float(weight) < _App._Settings.WEIGHTTHRESHOLD:
                            #self.GUI.updateWeightText("NO LOAD", "")
                            #self.GUI.updateNoneCodeImage()
                            #self.GUI.setNewLift(0, "")
                            self.GUI.newLiftSet('', '', None, None)
                            self.OLDWEIGHT = '0'
                            #_App.APPSTATE = APP_STATE.STATE_BEGIN_LIFT
                            #self.GUI.changeAppState()
                            return

                        self.OLDWEIGHT = weight

                        weightmode = ''

                        if 'KG' in response:
                            weightmode = 'KGS'
                        elif 'LB' in response:
                            weightmode = 'LBS'
                        elif response.endswith('L'):
                            weightmode = 'LBS'
                        elif response.endswith('K'):
                            weightmode = 'KGS'

                        #_App._Settings.WEIGHTMODE = weightmode
                        weight_code = weight + ' ' + weightmode
                        print("weight: ", weight_code)

                        EAN = barcode.get_barcode_class('code128')
                        ean = EAN(weight_code, writer = ImageWriter())
                        bar = ean.render()
                        barimg = bar.resize((240, 160), Image.ANTIALIAS)
                        pix_bar = QPixmap.fromImage(self.convert_barimg(barimg))

                        qr = qrcode.QRCode(version = 1,
                                            error_correction = qrcode.constants.ERROR_CORRECT_L,
                                            box_size = 7,
                                            border = 1,)
                        qr.add_data(weight_code)
                        qr.make(fit = True)
                        qrimg = qr.make_image(fill_color = "black", back_color = "white")
                        pix_qr = QPixmap.fromImage(self.convert_qrimg(qrimg))

                        #self.GUI.setNewLift(float(weight), weightmode)
                        self.GUI.newLiftSet(weight, weightmode, pix_bar, pix_qr)

                        '''
                        if _App._Settings.WEIGHTCODE == 'BARCODE':
                            self.GUI.updateBarCodeImage(pix_bar)
                        elif _App._Settings.WEIGHTCODE == 'QRCODE':
                            self.GUI.updateQrCodeImage(pix_qr)
                        else:
                            self.GUI.updateNoneCodeImage()
                        '''
                    else:
                        self.WCOUNT = self.WCOUNT + 1
            else:
                #print('Response contains M')
                return

        except Exception as e:
            print('Data Processing Error:', e)

    def convert_qrimg(self, pilimage):
        """converts a PIL image to QImage"""
        imageq = ImageQt(pilimage) #convert PIL image to a PIL.ImageQt object
        qimage = QImage(imageq) #cast PIL.ImageQt object to QImage object -that´s the trick!!!
        return qimage

    def convert_barimg(self, image):
        bytes_img = io.BytesIO()
        image.save(bytes_img, format='JPEG')

        qimg = QImage()
        qimg.loadFromData(bytes_img.getvalue())

        return qimg