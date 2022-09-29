from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys

from Config import _App

class Rs232ParserModeDialog(QtWidgets.QDialog):
    def __init__(self):
        super(Rs232ParserModeDialog, self).__init__()
        uic.loadUi('rs232parsermodedialog.ui', self)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WA_ShowWithoutActivating)
        self.setModal(True)

        self.btnDF1500.clicked.connect(self.slotDF1500)
        self.btnAvery.clicked.connect(self.slotAvery)
        self.btnRavas.clicked.connect(self.slotRavas)

        if _App._Settings.PARSERMODE == 'DF1500':
            self.btnDF1500.setStyleSheet('background-color: rgb(212, 212, 212); color: rgb(45, 161, 3)')
        elif _App._Settings.PARSERMODE == 'AVERY':
            self.btnAvery.setStyleSheet('background-color: rgb(212, 212, 212); color: rgb(45, 161, 3)')
        else:
            self.btnRavas.setStyleSheet('background-color: rgb(212, 212, 212); color: rgb(45, 161, 3)')

    def slotDF1500(self):
        _App._Settings.PARSERMODE = 'DF1500'
        self.accept()

    def slotAvery(self):
        _App._Settings.PARSERMODE = 'AVERY'
        self.accept()

    def slotRavas(self):
        _App._Settings.PARSERMODE = 'RAVAS'
        self.accept()