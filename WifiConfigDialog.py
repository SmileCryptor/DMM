from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
import os
import time
from subprocess import check_output
import subprocess
import threading
from wireless import Wireless

from Config import _App


class WifiConfigDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(WifiConfigDialog, self).__init__()
        uic.loadUi('wificonfigdialog.ui', self)

        self.parent = parent

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WA_ShowWithoutActivating)
        self.setModal(True)

        self.ssid = ''
        self.pwd = ''
        #self.wireless = Wireless()

        self.tick_connect = False
        #self.timer = QtCore.QTimer()

        #self.timer.setInterval(1000)
        #self.timer.timeout.connect(self.connect_timer)
        #self.timer.start(100)

        try:
            self.btnConnect.clicked.disconnect()
            self.btnAdd.clicked.disconnect()
        except:
            pass

        self.btnConnect.clicked.connect(self.on_btnConnect_clicked)
        self.btnAdd.clicked.connect(self.on_btnAdd_clicked)
        self.btnBack.clicked.connect(self.on_btnBack_clicked)

        t = threading.Thread(target=self.initListWidget)
        t.daemon = True
        t.start()
        
    def initListWidget(self):
        #self.listWidget.setEnabled(False)
        #self.btnConnect.setEnabled(False)
        #self.btnAdd.setEnabled(False)
        #self.btnBack.setEnabled(False)
        self.setEnabled(False)
        self.btnConnect.setText("Loading...")

        self.listWidget.clear()
        self.listWidget.addItems(list(filter(None, self.getWIFIList())))

        #self.listWidget.setEnabled(True)
        #self.btnConnect.setEnabled(True)
        #self.btnAdd.setEnabled(True)
        #self.btnBack.setEnabled(True)
        self.setEnabled(True)
        self.btnConnect.setText("Connect")

    def on_btnConnect_clicked(self):
        if ( self.listWidget.currentItem() is None ):
            return
        
        self.ssid = self.listWidget.currentItem().text()
        
        r = self.parent.MainWindow.showKeyboard(None, "Input wifi access password: " + self.ssid, QtWidgets.QLineEdit.Password)

        if r:
            self.pwd = _App.KEYBOARD_TEXT[0]

            _App.WIFI_SSID = self.ssid
            _App.WIFI_PWD = self.pwd
            _App.WIFICONNECTING = True

            return self.accept()
            #self.tick_connect = True
            #self.wifi_connect()
            #t = threading.Thread(target=self.wifi_connect)
            #t.daemon = True
            #t.start()

    def on_btnAdd_clicked(self):
        new_ssid = ""

        r = self.parent.MainWindow.showKeyboard(new_ssid, "Input new ssid")

        if r:
            new_ssid = _App.KEYBOARD_TEXT[0]
            if new_ssid != "":
                self.listWidget.addItem(new_ssid)

    def on_btnBack_clicked(self):
        self.reject()
            

    def getWIFIList(self):
        try:
            scanoutput = check_output(["iwlist", "wlan0", "scan"])

            ssid = []

            for line in scanoutput.split():
                line = line.decode("utf-8")
                # print(line)
                # if line[:5]  == "ESSID":
                #  ssid = line.split('"')[1]
                if line.startswith("ESSID"):
                    eid = line.split('\"')[1]
                    if eid not in ssid:
                        ssid.append(eid)
            if len(ssid) < 1:
                os.system('sudo ifconfig wlan0 down')
                os.system('sudo ifconfig wlan0 up')
                time.sleep(1)
                scanoutput = check_output(["iwlist", "wlan0", "scan"])

                ssid = []

                for line in scanoutput.split():
                    line = line.decode("utf-8")
                    # print(line)
                    # if line[:5] == "ESSID":
                    #  ssid = line.split('"')[1]
                    if line.startswith("ESSID"):
                        eid = line.split('\"')[1]
                        if eid not in ssid:
                            ssid.append(eid)
            return ssid
        except:
            return []
    
    def wifi_connect(self):
        self.btnConnect.setEnabled(False)
        self.listWidget.setEnabled(False)
        self.btnAdd.setEnabled(False)
        self.btnConnect.setText("Connecting...")
        try:
            print('connecting to wifi', self.ssid, '---', self.pwd)

            self.wireless.connect(ssid = self.ssid, password = self.pwd)

            if self.wireless.current() is None:
                raise Exception("wireless.connect() returned false")
            
            _App.WIFI_SSID = self.ssid
            _App.WIFI_PWD = self.pwd

            QMessageBox.information(None, "Wifi", "Wifi connected: " + self.ssid)

            self.btnConnect.setEnabled(True)
            self.listWidget.setEnabled(True)
            self.btnAdd.setEnabled(True)
            self.btnConnect.setText("Connect")

            return self.accept()
            
        except Exception as ex:
            print('WIFI CON ERROR:', ex)
            
            QMessageBox.warning(None, "Wifi", "Wifi connect faild: " + self.ssid)

            self.btnConnect.setEnabled(True)
            self.listWidget.setEnabled(True)
            self.btnAdd.setEnabled(True)
            self.btnConnect.setText("Connect")

    def connect_timer(self):
        if self.tick_connect is True:
            #self.btnConnect.setEnabled(False)
            #self.listWidget.setEnabled(False)
            #self.btnAdd.setEnabled(False)
            #self.btnBack.setEnabled(False)
            self.setEnabled(False)
            self.btnConnect.setText("Connecting...")
            try:
                print('connecting to wifi', self.ssid, '---', self.pwd)

                r = self.wireless.connect(ssid = self.ssid, password = self.pwd)

                if r is False:
                    raise Exception("wireless.connect() returned false")
                
                _App.WIFI_SSID = self.ssid
                _App.WIFI_PWD = self.pwd

                #QMessageBox.information(None, "Wifi", "Wifi connected: " + self.ssid)

                #self.btnConnect.setEnabled(True)
                #self.listWidget.setEnabled(True)
                #self.btnAdd.setEnabled(True)
                #self.btnBack.setEnabled(True)
                self.setEnabled(True)
                self.btnConnect.setText("Connect")

                self.tick_connect = False

                return self.accept()
                
            except Exception as ex:
                print('WIFI CON ERROR:', ex)
                #QMessageBox.warning(None, "Wifi", "Wifi connect faild: " + self.ssid)

                #self.btnConnect.setEnabled(True)
                #self.listWidget.setEnabled(True)
                #self.btnAdd.setEnabled(True)
                #self.btnBack.setEnabled(True)
                self.setEnabled(True)
                self.btnConnect.setText("Connect")
            
            self.tick_connect = False
    