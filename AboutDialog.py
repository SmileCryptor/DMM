from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QScroller
class AboutDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(AboutDialog, self).__init__()
        uic.loadUi('aboutdialog.ui', self)

        self.parent = parent

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        #self.setAttribute(QtCore.Qt.WA_AcceptTouchEvents, True)
        #self.btnBack.installEventFilter(self)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WA_ShowWithoutActivating)
        #self.setModal(True)
        self.setVisible(True)

        QScroller.grabGesture(self.scrollArea, QScroller.LeftMouseButtonGesture)

        self.ABOUT_TXT = 'about.txt'

        fp = open(self.ABOUT_TXT)
        data = fp.read()

        self.lblText.setText(data)
        #self.btnBack.setParent(self)
        #self.btnBack.setStyleSheet("color: rgb(240, 240, 240);background: rgb(101, 101, 101);border: 2px solid rgb(210, 210, 210);border-radius: 5px;")

        self.btnBack.clicked.connect(self.on_btnBack_clicked)

    def on_btnBack_clicked(self):
        self.reject()
    
    #def eventFilter(self, obj, event):
    #    if(event.type()>=2 and event.type()<=5 or event.type()>=194 and event.type()<=196):
    #        print('Touch event', event.type(), obj)
    #    return super(AboutDialog, self).eventFilter(obj, event)
