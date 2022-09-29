from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPainter, QTextDocument, QPixmap, QFont, QFontMetrics
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSize, QRect
import CodeModeDialog
import WifiConfigDialog
import EmailSetupDialog
import NetworkSetupDialog
import Rs232ParserModeDialog

import subprocess
import sys
import os

from Config import _App, APP_STATE

class BasicSettingsWidget(QtWidgets.QWidget):
    def __init__(self, MainWindow):
        super(BasicSettingsWidget, self).__init__()
        uic.loadUi('basicsettingwidget.ui', self)

        self.MainWindow = MainWindow

        self.btnBack.clicked.connect(self.MainWindow.setMainWidget)
        self.btnHome.clicked.connect(self.MainWindow.setMainWidget)

        self.btnWeightcode.clicked.connect(self.slotCodeClicked)
        self.btnWifi.clicked.connect(self.slotWifiClicked)
        self.btnEmailsetup.clicked.connect(self.slotEmailClicked)
        self.btnTruckid.clicked.connect(self.slotTruckidClicked)
        self.btnSetRWT.clicked.connect(self.slotRWTClicked)
        self.btnSetClientHost.clicked.connect(self.slotClientHostClicked)
        self.btnNetworkSetup.clicked.connect(self.slotNetSetupClicked)
        self.btnSetRS232Parser.clicked.connect(self.slotRS232ParserClicked)
        
    def slotCodeClicked(self):
        diag = CodeModeDialog.CodeModeDialog()
        r = diag.exec_()
        if r:
            self.MainWindow.mainWidget.changeCodeMode()

    def slotWifiClicked(self):
        diag = WifiConfigDialog.WifiConfigDialog(self)
        diag.exec_()

    def slotEmailClicked(self):
        diag = EmailSetupDialog.EmailSetupDialog(self)
        diag.exec_()

    def slotNetSetupClicked(self):
        diag = NetworkSetupDialog.NetworkSetupDialog(self)
        diag.exec_()

    def slotTruckidClicked(self):
        r = self.MainWindow.showKeyboard(_App._Settings.TRUCK_ID[3:], "Enter Truck ID")
        if r:
            if _App.KEYBOARD_TEXT[0] == '':
                _App._Settings.TRUCK_ID = ''
            else:
                new_id = "AL-" + _App.KEYBOARD_TEXT[0]

                if new_id == _App._Settings.TRUCK_ID:
                    return

                try:
                    #subprocess.run(['sudo', _App.APP_PATH + '/change_hostname.sh', new_id])
                    #subprocess.run(['./change_hostname.sh',  new_id])
                    subprocess.call(['sh', './change_hostname.sh', new_id])
                    #subprocess.call(['hostname', truckid])
                    
                    _App._Settings.TRUCK_ID = new_id

                    reply = QMessageBox.question(None, "Reboot System", "Sytem Reboot Required?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                    if reply == QMessageBox.Yes:
                        _App._Settings.save()
                        os.system('sudo shutdown -r now')
                except:
                    print('Hostname Edit Failed')

    def slotRWTClicked(self):
        r = self.MainWindow.showKeyboard(str(_App._Settings.WEIGHTTHRESHOLD), "Enter Record Weight Threshold")
        if r:
            if _App.KEYBOARD_TEXT[0] == ''  or _App.KEYBOARD_TEXT[0].isdigit() == False:
                QMessageBox.warning(None, "Input Error", "Please input valid number")
            else:
                _App._Settings.WEIGHTTHRESHOLD = int(_App.KEYBOARD_TEXT[0])

    def slotClientHostClicked(self):
        r = self.MainWindow.showKeyboard(str(_App._Settings.CLIENT_HOST), "Enter Client Host Address")
        if r:
            if _App.KEYBOARD_TEXT[0] == ''  or NetworkSetupDialog.validate_ip(_App.KEYBOARD_TEXT[0]) == False:
                QMessageBox.warning(None, "Input Error", "Please input valid ip address")
            else:
                _App._Settings.CLIENT_HOST = _App.KEYBOARD_TEXT[0]

    def slotRS232ParserClicked(self):
        diag = Rs232ParserModeDialog.Rs232ParserModeDialog()
        diag.exec_()

    def paintEvent(self, event):
        self.drawButtons()

    def drawButtons(self):
        self.drawWifiButton()
        self.drawWeightcodeButton()
        self.drawTruckidButton()
        self.drawRWTButton()
        self.drawMWTButton()
        self.drawClientHostButton()
        
    def drawWifiButton(self):
        html = ""
        if _App.WIFI_CONNECTION is False:
            html = "<div style='text-align: center;color: #d5d58c;font-size: 36px;font-weight: 500;'>WiFi</div><div style='text-align: center;color: #b51a00;font-size: 16px;margin-top: 30px;font-weight: 400;'>NOT CONNECTED</div>"
        else:
            html = "<div style='text-align: center;color: #d5d58c;font-size: 36px;font-weight: 500;'>WiFi</div><div style='text-align: center;color: #00c421;font-size: 16px;margin-top: 30px;font-weight: 400;'>{}</div>".format(_App.WIFI_SSID)

        self.drawContents(self.btnWifi, html)

    def drawWeightcodeButton(self):
        html = ""
        if _App._Settings.WEIGHTCODE == 'BARCODE':
            html = "<div style='text-align: center;color: #d5d58c;font-size: 24px;font-weight: 500;'>Weight as Code</div><div style='text-align: center;color: #00c421;font-size: 26px;font-weight: 500;margin-top: 10px;'>BARCODE</div>"
        elif _App._Settings.WEIGHTCODE == 'QRCODE':
            html = "<div style='text-align: center;color: #d5d58c;font-size: 24px;font-weight: 500;'>Weight as Code</div><div style='text-align: center;color: #00c421;font-size: 26px;font-weight: 500;margin-top: 10px;'>QR CODE</div>"
        else:
            html = "<div style='text-align: center;color: #d5d58c;font-size: 24px;font-weight: 500;'>Weight as Code</div><div style='text-align: center;color: #b51a00;font-size: 26px;font-weight: 500;margin-top: 10px;'>NO CODE</div>"
        
        self.drawContents(self.btnWeightcode, html)

    def drawTruckidButton(self):
        html = ""
        if _App._Settings.TRUCK_ID == '':
            html = "<div style='text-align: center;color: #d5d58c;font-size: 24px;font-weight: 500;'>TRUCK ID</div><div style='text-align: center;color: #b51a00;font-size: 26px;font-weight: 500;margin-top: 39px;'>NOT SET</div>"
        else:
            font = QFont("", 22)
            fm = QFontMetrics(font)
            pixelsWide = fm.width(_App._Settings.TRUCK_ID)

            if pixelsWide <= 180:
                html = "<div style='text-align: center;color: #d5d58c;font-size: 24px;font-weight: 500;'>TRUCK ID</div><div style='text-align: center;color: #00c421;font-size: 22px;font-weight: 500;margin-top: 40px;'>{}</div>".format(_App._Settings.TRUCK_ID)
            else:
                html = "<div style='text-align: center;color: #d5d58c;font-size: 24px;font-weight: 500;'>TRUCK ID</div><div style='text-align: center;color: #00c421;font-size: 22px;font-weight: 500;margin-top: 10px;'>{}</div>".format(_App._Settings.TRUCK_ID)
        self.drawContents(self.btnTruckid, html)
    
    def drawRWTButton(self):
        html = ""
        if _App._Settings.WEIGHTTHRESHOLD is None:
            html = "<div style='text-align: center;color: #9d4040;font-size: 22px;font-weight: 500;'>RECORD</div><div style='text-align: center;color: #d5d58c;font-size: 16px;font-weight: 500;'>WEIGHT THRESHOLD</div><div style='text-align: center;color: #b51a00;font-size: 26px;font-weight: 500;margin-top: 5px;'>NOT SET</div>"
        else:
            html = "<div style='text-align: center;color: #9d4040;font-size: 22px;font-weight: 500;'>RECORD</div><div style='text-align: center;color: #d5d58c;font-size: 16px;font-weight: 500;'>WEIGHT THRESHOLD</div><div style='text-align: center;color: #00c421;font-size: 26px;font-weight: 500;margin-top: 5px;'>{}</div>".format(_App._Settings.WEIGHTTHRESHOLD)
        self.drawContents(self.btnSetRWT, html)

    def drawMWTButton(self):
        html = "<div style='text-align: center;color: #a2e28d;font-size: 22px;font-weight: 500;'>MATCH</div><div style='text-align: center;color: #d5d58c;font-size: 16px;font-weight: 500;'>WEIGHT THRESHOLD</div><div style='text-align: center;color: #b51a00;font-size: 26px;font-weight: 500;margin-top: 5px;'>NOT SET</div>"
        self.drawContents(self.btnSetMWT, html)

    def drawClientHostButton(self):
        html = ""
        if _App._Settings.CLIENT_HOST == '':
            html = "<div style='text-align: center;color: #d5d58c;font-size: 24px;font-weight: 500;'>API</div><div style='text-align: center;color: #b51a00;font-size: 26px;font-weight: 500;margin-top: 40px;'>NOT SET</div>"
        else:
            html = "<div style='text-align: center;color: #d5d58c;font-size: 24px;font-weight: 500;'>API</div><div style='text-align: center;color: #00c421;font-size: 16px;font-weight: 500;margin-top: 50px;'>{}</div>".format(_App._Settings.CLIENT_HOST)

        self.drawContents(self.btnSetClientHost, html)


    def drawContents(self, button, html):
        text = QTextDocument()
        text.setHtml(html)
        text.setTextWidth(150)

        pixmap = QPixmap(150, 100)
        pixmap.fill( QtCore.Qt.transparent )
        painter = QPainter(pixmap)
        text.drawContents(painter)

        button.setIcon(QtGui.QIcon(pixmap))
        button.setIconSize(QSize(160, 120))
        painter.end()
