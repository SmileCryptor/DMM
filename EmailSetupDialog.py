from PyQt5 import QtCore, QtGui, QtWidgets, uic

from Config import _App

class EmailSetupDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(EmailSetupDialog, self).__init__()
        uic.loadUi('emaildialog.ui', self)

        self.parent = parent

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WA_ShowWithoutActivating)
        self.setModal(True)

        self.smtp_server = _App._Settings.SMTP_SERVER
        self.smtp_port = _App._Settings.SMTP_PORT
        self.smtp_email = _App._Settings.SMTP_EMAIL
        self.smtp_pwd = _App._Settings.SMTP_PWD
        self.smtp_ccemail = _App._Settings.SMTP_CCEMAIL

        self.editServer.setText(self.smtp_server)
        self.editPort.setText(str(self.smtp_port))
        self.editEmail.setText(self.smtp_email)
        self.editPassword.setText(self.smtp_pwd)
        self.editCcemail.setText(self.smtp_ccemail)

        self.btnBack.clicked.connect(self.on_btnBack_clicked)
        self.btnSave.clicked.connect(self.on_btnSave_clicked)
        self.editServer.installEventFilter(self)
        self.editPort.installEventFilter(self)
        self.editEmail.installEventFilter(self)
        self.editPassword.installEventFilter(self)
        self.editCcemail.installEventFilter(self)
    
    def mousePressEvent(self, event):
        print("Main Widget Mouse Press")
        super(EmailSetupDialog, self).mousePressEvent(event)

    def eventFilter(self, obj, event):
        if event.type() == event.MouseButtonPress:
            if obj == self.editServer:
                r = self.parent.MainWindow.showKeyboard(self.smtp_server, "Enter SMTP Server")
                if r:
                    self.smtp_server = _App.KEYBOARD_TEXT[0]
                    self.editServer.setText(self.smtp_server)
            elif obj == self.editPort:
                r = self.parent.MainWindow.showKeyboard(str(self.smtp_port), "Enter SMTP Port")
                if r:
                    self.smtp_port = int(_App.KEYBOARD_TEXT[0])
                    self.editPort.setText(str(self.smtp_port))
            elif obj == self.editEmail:
                r = self.parent.MainWindow.showKeyboard(self.smtp_email, "Enter Your Email")
                if r:
                    self.smtp_email = _App.KEYBOARD_TEXT[0]
                    self.editEmail.setText(self.smtp_email)
            elif obj == self.editPassword:
                r = self.parent.MainWindow.showKeyboard(self.smtp_pwd, "Enter Email Password", QtWidgets.QLineEdit.Password)
                if r:
                    self.smtp_pwd = _App.KEYBOARD_TEXT[0]
                    self.editPassword.setText(self.smtp_pwd)
            elif obj == self.editCcemail:
                r = self.parent.MainWindow.showKeyboard(self.smtp_ccemail, "Enter Recipient Email")
                if r:
                    self.smtp_ccemail = _App.KEYBOARD_TEXT[0]
                    self.editCcemail.setText(self.smtp_ccemail)


        # regardless, just do the default
        return super(EmailSetupDialog, self).eventFilter(obj, event)

    def on_btnBack_clicked(self):
        self.reject()

    def on_btnSave_clicked(self):
        _App._Settings.SMTP_SERVER = self.smtp_server
        _App._Settings.SMTP_PORT = self.smtp_port
        _App._Settings.SMTP_EMAIL = self.smtp_email
        _App._Settings.SMTP_PWD = self.smtp_pwd
        _App._Settings.SMTP_CCEMAIL = self.smtp_ccemail
        _App._Settings.saveSMTPConfig()

        self.accept()