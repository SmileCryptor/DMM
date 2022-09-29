import time
import threading
from icmplib import ping
from Config import _App
from Config import APP_STATE

class AppcheckerThread(threading.Thread):
    def __init__(self, GUI):
        threading.Thread.__init__(self)
        self.GUI = GUI

    def run(self):
        print('Entering Into App State Checker Thread')

        while _App.CHECKERSTAT:
            if _App.DEBUG_OUTPUT:
                print("App State Thread: app state: {}".format(_App.APPSTATE))

            if _App.LOG_TO_FILE:
                _App.append_to_log("App State Thread: app state: {}".format(_App.APPSTATE))
            
            if _App._Settings.TRUCK_ID == '':
                _App.APPSTATE = APP_STATE.STATE_NEED_TRUCKID
            elif _App.LoginState is False:
                _App.APPSTATE = APP_STATE.STATE_NEED_LOGIN

            if _App.MESSAGE_DURATION > 0:
                _App.MESSAGE_DURATION -= 1
            
            if _App.MESSAGE_DURATION <= 0:
                _App.MESSAGE_DURATION = 0
                _App.MESSAGE_ON = False

            self.checkClientAlive()
            
            self.GUI.changeAppState()

            time.sleep(1)

        print('Exiting From App State Checker Thread')

    def checkClientAlive(self):
        if _App._Settings.CLIENT_HOST == '':
            _App.CLIENT_HOST_ALIVE = False
        else:
            cli = ping(_App._Settings.CLIENT_HOST, 1, 1, 0.5)
            _App.CLIENT_HOST_ALIVE = cli.is_alive