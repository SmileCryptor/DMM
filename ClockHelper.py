from ClockTimeThread import ClockTimeThread

class ClockHelper:
    def __init__(self, GUI):
        self.GUI = GUI

    def startClock(self):
        ClockTimeThread(self.GUI).start()
