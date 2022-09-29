import sys, os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFontDatabase, QFont
import enum

from MainWidget import MainWidget
from ToolsWidget import ToolsWidget
import BasicSettingsWidget
import AppcheckerHelper
import APICallHelper
import ClockHelper
import WeightButtonHelper
import BarcodeScannerHelper
import KeyboardWidget
import WirelessHelper

from Config import _App
from DBHelper import _DB

class CurrentWidget(enum.Enum):
    NONE                    = -1
    MAIN_WIDGET             = 0
    TOOLS_WIDGET            = 1
    BASIC_SETTING_WIDGET    = 2
    KEYBOARD_WIDGET         = 3

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()

        self.currentWidget = CurrentWidget.NONE.value

        self.mainWidget = MainWidget(self)
        self.toolsWidget = ToolsWidget(self)
        self.basicsettingsWidget = BasicSettingsWidget.BasicSettingsWidget(self)
        self.keyboard = KeyboardWidget.KeyboardWidget(self)

        self.mainStacked.addWidget(self.mainWidget)
        self.mainStacked.addWidget(self.toolsWidget.toolsWidget)
        self.mainStacked.addWidget(self.basicsettingsWidget)
        #self.mainStacked.addWidget(self.keyboard)
       
        self.setMainWidget()
        #self.setToolsWidget()

        #self.initStatVariables()
        #self.setWeightFont()
        self.initHelperClass()


    #def initStatVariables(self):
        #self.TRUCKID = ''
        #self.CURRENTWEIGHT = '0'
        #self.DOCID = ''

    def setWeightFont(self):
        QFontDatabase.addApplicationFont("./res/font/DJB Get Digital.ttf")
        your_ttf_font = QFont("DJB Get Digital", 65)
        # your_ttf_font.setBold(True)
        self.mainWidget.lblWeight.setFont(your_ttf_font)
        # DMMMainUI.closeEvent(self.closeEvent1)

    def initHelperClass(self):
        AppcheckerHelper.AppcheckerThread(self.mainWidget).start()
        APICallHelper.APICallThread(self.mainWidget).start()
        ClockHelper.ClockHelper(self.mainWidget).startClock()
        BarcodeScannerHelper.BarcodeScannerHelper(self.mainWidget).startScan()
        WirelessHelper.WirelessThread(self.mainWidget).start()
        self.WBHelper = WeightButtonHelper.WeightButtonHelper(self.mainWidget)
        print(_App._Settings.PARSERMODE)
        if _App._Settings.SERIALMODE == 'HX711':
            self.WBHelper.readHX711()
        else:
            self.WBHelper.readRS232()

    def setMainWidget(self):
        self.mainStacked.setCurrentIndex(CurrentWidget.MAIN_WIDGET.value)
        self.currentWidget = CurrentWidget.MAIN_WIDGET.value

    def setToolsWidget(self):
        self.mainStacked.setCurrentIndex(CurrentWidget.TOOLS_WIDGET.value)
        self.currentWidget = CurrentWidget.TOOLS_WIDGET.value

    def setBasicSettingWidget(self):
        self.mainStacked.setCurrentIndex(CurrentWidget.BASIC_SETTING_WIDGET.value)
        self.currentWidget = CurrentWidget.BASIC_SETTING_WIDGET.value

    def showKeyboard(self, Src, LabelText, EchoMode = QtWidgets.QLineEdit.Normal):
        #self.mainStacked.setCurrentIndex(CurrentWidget.KEYBOARD_WIDGET.value)
        self.keyboard.initKeyboard(Src, LabelText, EchoMode)
        self.keyboard.show()
        return self.keyboard.exec_()
        

    def hideKeyboard(self):
        self.mainStacked.setCurrentIndex(self.currentWidget)

    def closeEvent(self, event):
        result = QtWidgets.QMessageBox.question(self,
                      "Confirm Exit...",
                      "Are you sure you want to exit ?",
                      QtWidgets.QMessageBox.Yes| QtWidgets.QMessageBox.No)
        event.ignore()

        if result == QtWidgets.QMessageBox.Yes:
            event.accept()

            print('Exiting Program Loop')
            _App.CHECKERSTAT = False
            _App.APICALLSTAT = False
            _App.HX711STAT = False
            _App.RS232STAT = False
            _App.BCSCANSTAT = False
            _App.TIMESTAT = False
            _App.WIFISTAT = False
            _DB.closeDB()
            _App._Settings.save()
            
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:

            '''
            if self.mainWidget.isMessageEmpty() is False:
                self.mainWidget.showMessage("Info", "PENDING LIFTS, PLEASE WAIT...", 3)
                event.ignore()
                return
            '''

            self.close()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1024, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(1024, 600))
        self.setMaximumSize(QtCore.QSize(1024, 600))
        self.setStyleSheet("QMainWindow#MainWindow {background-color: black;}")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, -10, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainStacked = QtWidgets.QStackedWidget(self.centralwidget)
        self.mainStacked.setObjectName("mainStacked")

        self.verticalLayout.addWidget(self.mainStacked)
        self.setCentralWidget(self.centralwidget)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.CustomizeWindowHint)
        #self.showMaximized()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "DMM"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
