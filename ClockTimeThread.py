import time
import threading
from datetime import datetime
from Config import _App


class ClockTimeThread(threading.Thread):
    def __init__(self, GUI):
        threading.Thread.__init__(self)
        self.GUI = GUI
        self.OLDTIME = ''

    def run(self):
        print('Entering Clock Time Thread')

        while _App.TIMESTAT:
            now = datetime.now()
            currentTime = now.strftime("%H:%M %p")
            currentDate = now.strftime("%A, %B %d, %Y")
            timestamp = currentTime + ' ' + currentDate

            if _App.DEBUG_OUTPUT:
                print('Clock Time Thread: {}'.format(timestamp))

            if _App.LOG_TO_FILE:
                _App.append_to_log('Clock Time Thread: {}'.format(timestamp))

            if timestamp != self.OLDTIME:
                self.GUI.updateTimeText(timestamp)
                self.OLDTIME = timestamp
            time.sleep(1)
        
        print('Exiting Clock Time Thread')