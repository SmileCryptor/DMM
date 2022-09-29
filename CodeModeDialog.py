from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys

from Config import _App

class CodeModeDialog(QtWidgets.QDialog):
    def __init__(self):
        super(CodeModeDialog, self).__init__()
        uic.loadUi('codemodedialog.ui', self)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WA_ShowWithoutActivating)
        self.setModal(True)

        self.btnCodeNone.clicked.connect(self.slotCodeNone)
        self.btnCodeBar.clicked.connect(self.slotCodeBarcode)
        self.btnCodeQr.clicked.connect(self.slotCodeQrcode)

    def slotCodeNone(self):
        _App._Settings.WEIGHTCODE = None
        self.accept()

    def slotCodeBarcode(self):
        _App._Settings.WEIGHTCODE = 'BARCODE'
        self.accept()

    def slotCodeQrcode(self):
        _App._Settings.WEIGHTCODE = 'QRCODE'
        self.accept()
