import time
import threading
from Config import _App

from wireless import Wireless


class WirelessThread(threading.Thread):
    def __init__(self, GUI):
        threading.Thread.__init__(self)
        self.GUI = GUI
        self.wireless = Wireless()

    def run(self):
        print('Entering Wireless Thread...')
        
        while _App.WIFISTAT:
            if _App.DEBUG_OUTPUT:
                print('Wireless Thread: connecting is {}'.format(_App.WIFICONNECTING))

            if _App.LOG_TO_FILE:
                _App.append_to_log('Wireless Thread: connecting is {}'.format(_App.WIFICONNECTING))

            if _App.WIFICONNECTING is True:
                try:
                    print('connecting to wifi', _App.WIFI_SSID, '---', _App.WIFI_PWD)
                    self.wireless.connect(ssid = _App.WIFI_SSID, password = _App.WIFI_PWD)

                except Exception as ex:
                    print('WIFI CON ERROR:', ex)

            _App.WIFICONNECTING = False
            

            if ( self.wireless.current() is not None):
                print("wifi connected")
                _App.WIFI_SSID = self.wireless.current()
                _App.WIFI_CONNECTION = True
            else:
                print("wifi connection is none")
                _App.WIFI_SSID = ''
                _App.WIFI_CONNECTION = False

            self.GUI.setWifiIcon()
                    
            time.sleep(10)

        print('Exiting Wireless Thread...')
        