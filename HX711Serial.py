import serial
import time
import SerialConfig
import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
import os

class HX711Serial:

    def __init__(self):
        try:
            config = SerialConfig.SerialConfig()
            self.Hx711 = None
            self.INTERVAL = config.interval
            self.WEIGHTCHECKING = config.weightChecking
            self.DOUT_PIN = (int)(config.doutpin)
            self.PD_SCK_PIN = (int)(config.pdsckpin)
            self.GAIN = (int)(config.gain)
            self.CHANNEL = config.channel
            self.ROUNDOFF = config.roundoff
        except:
            print('Config Serial Error')


    def checkSerial(self):
        stat = False
        try:
            GPIO.setmode(GPIO.BCM)
            hx = HX711(dout_pin=self.DOUT_PIN, pd_sck_pin=self.PD_SCK_PIN,gain_channel_A=self.GAIN,select_channel=self.CHANNEL)
            hx.reset()
            err = hx.zero()
            if err:
                raise ValueError('Tare is unsuccessful.')
                #printLog('Tare is unsuccessful.')
            reading = hx.get_raw_data_mean()
            if reading:  # always check if you get correct value or only False
                # now the value is close to 0
                print('Data subtracted by offset but still not converted to units:',
                      reading)
                #printLog('Data subtracted by offset but still not converted to units:')
                #printLog('Initialization Done')
                #printLog('Put known weight on the scale, textbox, and then press Calibrate')
                stat = True
                self.Hx711 = hx
            else:
                print('invalid data', reading)
                #printLog('Invalid data')
                stat = False
        except Exception as e:
            stat = False
            print("error open hx711: " + str(e))
        finally:
            return stat

    def checkSerialConfig(self):
        stat = False
        try:
            if os.path.exists('./db/hx711.dat'):
                new_file = open("./db/hx711.dat", mode="rb")
                line = new_file.readline()
                new_file.close()
                print('hx711 dat Line:',line)
                if line:
                    ratio = line.decode('UTF-8')
                    GPIO.setmode(GPIO.BCM)
                    hx = HX711(dout_pin=self.DOUT_PIN, pd_sck_pin=self.PD_SCK_PIN,gain_channel_A=self.GAIN,select_channel=self.CHANNEL)
                    #hx.reset()
                    err = hx.zero()
                    if err:
                        raise ValueError('Tare is unsuccessful.')
                        #printLog('Tare is unsuccessful.')
                    reading = hx.get_raw_data_mean()
                    if reading:  # always check if you get correct value or only False
                        # now the value is close to 0
                        print('Data subtracted by offset but still not converted to units:',
                              reading)
                        #printLog('Data subtracted by offset but still not converted to units:')
                        #printLog('Initialization Done')
                        hx.set_scale_ratio((float)(ratio))  # set ratio for current channel
                        print('Ratio is set.')
                        #printLog('Calibration Done')
                        self.Hx711 = hx
                        stat = True
                    else:
                        print('invalid data', reading)
                        #printLog('Invalid data')
                        stat = False
        except Exception as e:
            stat = False
            print("error open hx711: " + str(e))
        finally:
            return stat

