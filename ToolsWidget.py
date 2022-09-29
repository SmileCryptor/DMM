# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'toolwidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QInputDialog

from glob import glob
import os
from datetime import datetime

from Config import _App
import GenCSVKeepData
import EmailSetup
from Calculator import Calculator
import AboutDialog

class ToolsWidget(object):
    def __init__(self, MainWindow):
        self.toolsWidget = QtWidgets.QWidget()
        self.setupUi(self.toolsWidget)

        self.MainWindow = MainWindow

        self.btnBack.clicked.connect(self.MainWindow.setMainWidget)

        self.btnCopy.clicked.connect(self.slotCopyCsvClicked)
        self.btnEmail.clicked.connect(self.slotEmailCsvClicked)
        self.btnCalc.clicked.connect(self.slotCalcClicked)
        self.btnInfo.clicked.connect(self.slotInfoClicked)
        self.btnClearLog.clicked.connect(self.slotClearLogClicked)

    def getSDPath(self):
        path = '/media/pi/*/'
        dirs = glob(path)
        if len(dirs) > 0:
            path = dirs[0]
        else:
            path = os.getcwd()
            path = path + '/'
        now = datetime.now()
        date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
        filepath = path + 'csv/ALL_' + date_time + '.csv'
        return filepath

    def slotCopyCsvClicked(self):
        directorypath = self.getSDPath()
        if not directorypath:
            print("Task Error", "Error Occured")
        else:
            csvc = GenCSVKeepData.GenCSVKeepData()
            csvc.doTask(directorypath)
            print("Data Task", "CSV File Created and Database Kept\nPath:" + directorypath)

    def slotEmailCsvClicked(self):
        if _App._Settings.SMTP_CCEMAIL == '':
            QMessageBox.warning(None, "SMTP Config Error", "Please confirm SMTP config first.")
            return

        text, ok = QInputDialog.getText(None, 'SMTP CCEmail', 'Enter email to:', QtWidgets.QLineEdit.Normal, _App._Settings.SMTP_CCEMAIL)
        #reply = QMessageBox.question(None, "CSV Report", "Do you report to {}?".format(_App._Settings.SMTP_CCEMAIL), QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if ok:
            try:
                _App._Settings.SMTP_CCEMAIL = text
                truckid = _App._Settings.TRUCK_ID
                now = datetime.now()
                date_time = now.strftime("%m/%d/%Y-%H:%M:%S")

                subject = truckid + '-Weight Report ' + date_time
                message = 'Please see attached CSV Weight report taken for ' + truckid + ' - ' + date_time

                filepath = './csv/' + truckid + '.csv'
                csvc = GenCSVKeepData.GenCSVKeepData()
                csvc.doTask(filepath)
                attachments = [filepath]
                
                [smtp_server, smtp_port, smtp_email, smtp_pwd, smtp_ccemail] = _App._Settings.getSMTPConfig()
                print('Connecting to server...')
                server = EmailSetup.EmailConnection(smtp_server, smtp_port, smtp_email, smtp_pwd)
                print('Preparing the email...')
                email = EmailSetup.Email(from_='<%s>' % (smtp_email),  # you can pass only email
                                        to='<%s>' % (smtp_ccemail),  # you can pass only email
                                        subject=subject, message=message, attachments=attachments)
                print('Sending...')
                server.send(email)
                print('Disconnecting...')
                server.close()
                _App._Settings.saveSMTPConfig()
                
                print('Done!')
                QMessageBox.information(None, "Email Task", "Email Sent Successfully!!!")
                
            except:
                print('Error Occured')
                QMessageBox.information(None, "Email Task", "Sorry !!! Email Sent Unsucessfull")

    def slotCalcClicked(self):
        calc = Calculator()
        calc.show()
        calc.exec_()

    def slotInfoClicked(self):
        diag = AboutDialog.AboutDialog(self)
        diag.exec_()

    def slotClearLogClicked(self):
        if self.MainWindow.mainWidget.clearLog() is False:
            QMessageBox.information(None, "Clear Log", "Failed! You need to logout first")


    def setupUi(self, ToolsWidget):
        ToolsWidget.setObjectName("ToolsWidget")
        ToolsWidget.resize(1024, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ToolsWidget.sizePolicy().hasHeightForWidth())
        ToolsWidget.setSizePolicy(sizePolicy)
        ToolsWidget.setMinimumSize(QtCore.QSize(1024, 600))
        ToolsWidget.setMaximumSize(QtCore.QSize(1024, 600))
        ToolsWidget.setStyleSheet("QWidget#ToolWidget {background-color: black;} QToolButton {background-color: transparent;};")
        self.verticalLayout = QtWidgets.QVBoxLayout(ToolsWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(40, 24, 40, -1)
        self.gridLayout.setSpacing(50)
        self.gridLayout.setObjectName("gridLayout")
        self.btnCopy = QtWidgets.QToolButton(ToolsWidget)
        self.btnCopy.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/gui/tools_copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCopy.setIcon(icon)
        self.btnCopy.setIconSize(QtCore.QSize(200, 148))
        self.btnCopy.setObjectName("btnCopy")
        self.gridLayout.addWidget(self.btnCopy, 0, 1, 1, 1)
        self.btnEmail = QtWidgets.QToolButton(ToolsWidget)
        self.btnEmail.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("res/gui/tools_email.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnEmail.setIcon(icon1)
        self.btnEmail.setIconSize(QtCore.QSize(200, 148))
        self.btnEmail.setObjectName("btnEmail")
        self.gridLayout.addWidget(self.btnEmail, 0, 0, 1, 1)
        self.btnCalc = QtWidgets.QToolButton(ToolsWidget)
        self.btnCalc.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnCalc.setStyleSheet("background-color: transparent")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("res/gui/tools_calculator.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCalc.setIcon(icon2)
        self.btnCalc.setIconSize(QtCore.QSize(200, 148))
        self.btnCalc.setObjectName("btnCalc")
        self.gridLayout.addWidget(self.btnCalc, 1, 0, 1, 1)
        self.btnDiagnostics = QtWidgets.QToolButton(ToolsWidget)
        self.btnDiagnostics.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("res/gui/tools_diagnostics.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDiagnostics.setIcon(icon3)
        self.btnDiagnostics.setIconSize(QtCore.QSize(200, 148))
        self.btnDiagnostics.setObjectName("btnDiagnostics")
        self.gridLayout.addWidget(self.btnDiagnostics, 0, 2, 1, 1)
        self.btnInfo = QtWidgets.QToolButton(ToolsWidget)
        self.btnInfo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("res/gui/tools_info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnInfo.setIcon(icon4)
        self.btnInfo.setIconSize(QtCore.QSize(200, 148))
        self.btnInfo.setObjectName("btnInfo")
        self.gridLayout.addWidget(self.btnInfo, 0, 3, 1, 1)
        self.btnClearLog = QtWidgets.QToolButton(ToolsWidget)
        self.btnClearLog.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("res/gui/tools_clearlog.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnClearLog.setIcon(icon5)
        self.btnClearLog.setIconSize(QtCore.QSize(200, 148))
        self.btnClearLog.setObjectName("btnClearLog")
        self.gridLayout.addWidget(self.btnClearLog, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 76, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(12, -1, 12, 7)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnBack = QtWidgets.QToolButton(ToolsWidget)
        self.btnBack.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("res/gui/button_back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnBack.setIcon(icon5)
        self.btnBack.setIconSize(QtCore.QSize(103, 103))
        self.btnBack.setObjectName("btnBack")
        self.horizontalLayout.addWidget(self.btnBack)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label = QtWidgets.QLabel(ToolsWidget)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("res/gui/img_tools.png"))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.btnHome = QtWidgets.QToolButton(ToolsWidget)
        self.btnHome.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("res/gui/button_home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnHome.setIcon(icon6)
        self.btnHome.setIconSize(QtCore.QSize(103, 103))
        self.btnHome.setObjectName("btnHome")
        self.horizontalLayout.addWidget(self.btnHome)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ToolsWidget)
        QtCore.QMetaObject.connectSlotsByName(ToolsWidget)

    def retranslateUi(self, ToolsWidget):
        _translate = QtCore.QCoreApplication.translate
        ToolsWidget.setWindowTitle(_translate("ToolsWidget", "ToolsWidget"))
        self.btnCopy.setText(_translate("ToolsWidget", "..."))
        self.btnEmail.setText(_translate("ToolsWidget", "..."))
        self.btnCalc.setText(_translate("ToolsWidget", "..."))
        self.btnDiagnostics.setText(_translate("ToolsWidget", "..."))
        self.btnInfo.setText(_translate("ToolsWidget", "..."))
        self.btnBack.setText(_translate("ToolsWidget", "..."))
        self.btnHome.setText(_translate("ToolsWidget", "..."))
