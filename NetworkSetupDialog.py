from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox

import os
import subprocess
from Config import _App

def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


class NetworkSetupDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(NetworkSetupDialog, self).__init__()
        uic.loadUi('networkdialog.ui', self)

        self.parent = parent

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WA_ShowWithoutActivating)
        self.setModal(True)

        self.net_type = 0
        self.net_ipaddr = ''
        self.net_mask = ''
        self.net_gateway = ''
        self.net_dns1 = ''
        self.net_dns2 = ''

        self.cmbInterface.currentIndexChanged.connect(self.on_cmbInterface_changed)

        self.btnBack.clicked.connect(self.on_btnBack_clicked)
        self.btnSave.clicked.connect(self.on_btnSave_clicked)
        self.editIpaddr.installEventFilter(self)
        self.editMask.installEventFilter(self)
        self.editGateway.installEventFilter(self)
        self.editDns1.installEventFilter(self)
        self.editDns2.installEventFilter(self)

    def on_cmbInterface_changed(self, i):
        if i == 0:
            self.editIpaddr.setEnabled(False)
            self.editMask.setEnabled(False)
            self.editGateway.setEnabled(False)
            self.editDns1.setEnabled(False)
            self.editDns2.setEnabled(False)

            self.net_type = 0
        elif i == 1:
            self.editIpaddr.setEnabled(True)
            self.editMask.setEnabled(True)
            self.editGateway.setEnabled(True)
            self.editDns1.setEnabled(True)
            self.editDns2.setEnabled(True)

            self.net_type = 1

    def mousePressEvent(self, event):
        print("Main Widget Mouse Press")
        super(NetworkSetupDialog, self).mousePressEvent(event)

    def eventFilter(self, obj, event):
        if event.type() == event.MouseButtonPress:
            if obj == self.editIpaddr and self.net_type == 1:
                r = self.parent.MainWindow.showKeyboard(self.net_ipaddr, "Enter IP Address")
                if r:
                    if validate_ip(_App.KEYBOARD_TEXT[0]) is True:
                        self.net_ipaddr = _App.KEYBOARD_TEXT[0]
                        self.editIpaddr.setText(self.net_ipaddr)
                    else:
                        QMessageBox.warning(None, "Input Error", "Please input valid ip address")
            elif obj == self.editMask and self.net_type == 1:
                r = self.parent.MainWindow.showKeyboard(str(self.net_mask), "Enter Subnet Mask")
                if r:
                    if validate_ip(_App.KEYBOARD_TEXT[0]) is True:
                        self.net_mask = _App.KEYBOARD_TEXT[0]
                        self.editMask.setText(str(self.net_mask))
                    else:
                        QMessageBox.warning(None, "Input Error", "Please input valid ip address")
            elif obj == self.editGateway and self.net_type == 1:
                r = self.parent.MainWindow.showKeyboard(self.net_gateway, "Enter Default Gateway")
                if r:
                    if validate_ip(_App.KEYBOARD_TEXT[0]) is True:
                        self.net_gateway = _App.KEYBOARD_TEXT[0]
                        self.editGateway.setText(self.net_gateway)
                    else:
                        QMessageBox.warning(None, "Input Error", "Please input valid ip address")
            elif obj == self.editDns1 and self.net_type == 1:
                r = self.parent.MainWindow.showKeyboard(self.net_dns1, "Enter DNS1")
                if r:
                    if validate_ip(_App.KEYBOARD_TEXT[0]) is True:
                        self.net_dns1 = _App.KEYBOARD_TEXT[0]
                        self.editDns1.setText(self.net_dns1)
                    else:
                        QMessageBox.warning(None, "Input Error", "Please input valid ip address")
            elif obj == self.editDns2 and self.net_type == 1:
                r = self.parent.MainWindow.showKeyboard(self.net_dns2, "Enter DNS2")
                if r:
                    if validate_ip(_App.KEYBOARD_TEXT[0]) is True:
                        self.net_dns2 = _App.KEYBOARD_TEXT[0]
                        self.editDns2.setText(self.net_dns2)
                    else:
                        QMessageBox.warning(None, "Input Error", "Please input valid ip address")


        # regardless, just do the default
        return super(NetworkSetupDialog, self).eventFilter(obj, event)


    def on_btnBack_clicked(self):
        self.reject()

    def on_btnSave_clicked(self):
        if self.net_type == 0:
            print("SET DHCP")
            os.system("sudo dhclient -r wlan0")
        elif self.net_type == 1:
            print("SET STATIC IP")
            if self.net_ipaddr != "":
                subprocess.run(["sudo", "ifconfig", "wlan0", self.net_ipaddr, "up"])

            if self.net_mask != "":
                subprocess.run(["sudo", "ifconfig", "wlan0", "netmask", self.net_mask])

            if self.net_gateway != "":
                subprocess.run(["sudo", "route", "add", self.net_gateway, "wlan0"])

            if self.net_dns1 != "":
                #subprocess.run(["sudo", "echo", "'nameserver {}'".format(self.net_dns1), ">", "/etc/resolv.conf"])
                subprocess.call(['sh', './set_dns.sh', self.net_dns1])

            if self.net_dns2 != "":
                #subprocess.run(["sudo", "echo", "'nameserver {}'".format(self.net_dns1), ">", "/etc/resolv.conf"])
                subprocess.call(['sh', './set_dns.sh', self.net_dns2])

            #call(["ifconfig", "eth0", self.net_ipaddr, "netmask", self.net_mask, "broadcast", "192.168.2.255"])

        self.accept()