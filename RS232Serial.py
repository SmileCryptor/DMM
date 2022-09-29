import serial
import time
import SerialConfig

class RS232Serial:
    def __init__(self):
        try:
            config = SerialConfig.SerialConfig()
            self.ser = serial.Serial()
            self.ser.port = config.port
            self.ser.baudrate = config.baudrate
            self.ser.bytesize = config.bytesize
            self.ser.parity = config.parity
            self.ser.stopbits = config.stopbits
            self.ser.timeout = config.timeout
            self.ser.xonxoff = config.xonxoff
            self.ser.rtscts = config.rtscts
            self.ser.dsrdtr = config.dsrdtr
            self.ser.writeTimeout = config.writeTimeout
            self.INTERVAL = config.interval
        except:
            print('Config Serial Error')


    def checkSerial(self):
        stat = False
        try:
            self.ser.open()
            print('Serial Port Found!!!')
            stat = True
        except Exception as e:
            print("error open serial port: " + str(e))
        finally:
            return stat
