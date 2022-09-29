import sys
import threading
import time
import random
#import readchar

from Config import _App
from Config import APP_STATE

hid = { 4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm', 17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y', 29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ', 45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';' , 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'  }

hid2 = { 4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M', 17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y', 29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 44: ' ', 45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':' , 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'  }


class BarcodeScannerThread(threading.Thread):
    def __init__(self, GUI):
        threading.Thread.__init__(self)
        self.GUI = GUI

        if _App.DEBUG is False:
            self.fp = open("/dev/hidraw1", "rb")
        else:
            fb = open("barcodes.txt")

            self.list_barcodes = []
            self.count = 0
            for line in fb:
                bc = line.strip()
                self.list_barcodes.append(bc)
                self.count += 1

    def run(self):
        print('Entering Barcode Scan Thread')

        if _App.LOG_TO_FILE:
            _App.append_to_log("BarcodeThread-Started")

        while _App.BCSCANSTAT:
            if _App.DEBUG_OUTPUT:
                print('Barcode Scanner Thread: running...')

            if _App.LOG_TO_FILE:
                _App.append_to_log('Barcode Scanner Thread: running...')
            
            if _App.APPSTATE != APP_STATE.STATE_SCAN_BARCODE:
                time.sleep(1)
                continue

            if _App.DEBUG is True:
                rval = random.randint(0, self.count - 1)
                barcode_in = self.list_barcodes[rval]
                print("Scan Barcode: ", barcode_in)

                self.doProcessing(barcode_in)
                time.sleep(1)
            else:
                barcode_in = self.scan()
                print("Scan Barcode: ", barcode_in)
                if _App.LOG_TO_FILE:
                    _App.append_to_log("BarcodeThread-Scaned barcode")

                self.doProcessing(barcode_in)
                time.sleep(0.1)

        if _App.DEBUG is False:
            self.fp.close()

        print("Exiting Barcode Scan Thread")

    def doProcessing(self, barcode):
        #self.GUI.addFBItem(barcode)
        self.GUI.newItemScanned(barcode)

    def scan(self):
        ss = ""
        shift = False

        done = False

        while ( not done ) and _App.BCSCANSTAT:
            ## Get the character from the HID
            buffer = self.fp.read(8)
            '''
            buffer = ''
            while ( len(buffer) != 8 and _App.BCSCANSTAT ):
                print('readchar.readchar()')
                buffer += str(readchar.readchar())
                print('readchar.readchar()1')

            if not _App.BCSCANSTAT:
                break
            '''
            for c in buffer:
                if type(c) == int:
                    c = chr(c)
                    
                if ord(c) > 0:
                    try:

                        ##  40 is carriage return which signifies
                        ##  we are done looking for characters
                        if int(ord(c)) == 40:
                            done = True
                            break

                        ##  If we are shifted then we have to 
                        ##  use the hid2 characters.
                        if shift: 

                            ## If it is a '2' then it is the shift key
                            if int(ord(c)) == 2 :
                                shift = True

                            ## if not a 2 then lookup the mapping
                            else:
                                ss += hid2[ int(ord(c)) ]
                                shift = False

                        ##  If we are not shifted then use
                        ##  the hid characters

                        else:

                            ## If it is a '2' then it is the shift key
                            if int(ord(c)) == 2 :
                                shift = True

                            ## if not a 2 then lookup the mapping
                            else:
                                ss += hid[ int(ord(c)) ]
                    except KeyError:
                        ss += ""
        #self.fp.truncate()

        return ss
