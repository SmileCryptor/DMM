"""
Generated python code using PyQt5 Designer. Need to fix bad formatting
as this is generated UI code after making the UI using PyQt5 Designer.
"""

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Calculator(object):
    def setupUi(self, Calculator):
        Calculator.setObjectName("Calculator")
        Calculator.setEnabled(True)
        Calculator.resize(560, 531)

        stylesheet = "QDialog { background-color: rgb(26,27,40); } QPushButton { background-color: rgb(30,36,53); border-radius: 20px; color: white; } QPushButton:pressed { background-color: rgb(40, 46, 63); } "
        stylesheet1 = "QPushButton{ background-color: rgb(82, 201, 220); } QPushButton:pressed { background-color: rgb(102, 221, 240); }"
        stylesheet2 = "QPushButton{ background-color: rgb(145, 25, 30); color: rgb(216, 62, 70); } QPushButton:pressed { background-color: rgb(165, 45, 50); }"

        Calculator.setStyleSheet(stylesheet)

        self.Five = QtWidgets.QPushButton(Calculator)
        self.Five.setGeometry(QtCore.QRect(120, 230, 101, 91))

        font = QtGui.QFont()
        font.setFamily("STIX")
        font.setPointSize(24)

        self.Five.setFont(font)
        self.Five.setObjectName("Five")

        self.Six = QtWidgets.QPushButton(Calculator)
        self.Six.setGeometry(QtCore.QRect(230, 230, 101, 91))

        font = QtGui.QFont()
        font.setFamily("STIX")
        font.setPointSize(24)

        self.Six.setFont(font)
        self.Six.setObjectName("Six")

        self.Seven = QtWidgets.QPushButton(Calculator)
        self.Seven.setGeometry(QtCore.QRect(10, 130, 101, 91))

        font = QtGui.QFont()
        font.setFamily("STIX")
        font.setPointSize(24)

        self.Seven.setFont(font)
        self.Seven.setObjectName("Seven")

        #self.Sqrt = QtWidgets.QPushButton(Calculator)
        #self.Sqrt.setGeometry(QtCore.QRect(450, 230, 101, 91))

        #font = QtGui.QFont()
        #font.setFamily("STIX")
        #font.setPointSize(24)

        #self.Sqrt.setFont(font)
        #self.Sqrt.setObjectName("Sqrt")
        #self.Sqrt.setStyleSheet(stylesheet1)

        self.Multiply = QtWidgets.QPushButton(Calculator)
        self.Multiply.setGeometry(QtCore.QRect(340, 230, 101, 91))

        font = QtGui.QFont()
        font.setFamily("STIX")
        font.setPointSize(24)

        self.Multiply.setFont(font)
        self.Multiply.setObjectName("Multiply")
        self.Multiply.setStyleSheet(stylesheet1)

        self.Decimal = QtWidgets.QPushButton(Calculator)
        self.Decimal.setGeometry(QtCore.QRect(120, 430, 101, 91))

        font = QtGui.QFont()
        font.setFamily("STIX")
        font.setPointSize(24)

        self.Decimal.setFont(font)
        self.Decimal.setObjectName("Decimal")

        self.Eight = QtWidgets.QPushButton(Calculator)
        self.Eight.setGeometry(QtCore.QRect(120, 130, 101, 91))

        font = QtGui.QFont()
        font.setFamily("STIX")
        font.setPointSize(24)

        self.Eight.setFont(font)
        self.Eight.setObjectName("Eight")

        self.Divide = QtWidgets.QPushButton(Calculator)
        self.Divide.setGeometry(QtCore.QRect(340, 130, 101, 91))

        font = QtGui.QFont()
        font.setFamily("STIX")
        font.setPointSize(24)

        self.Divide.setFont(font)
        self.Divide.setObjectName("Divide")
        self.Divide.setStyleSheet(stylesheet1)

        self.PlusMinus = QtWidgets.QPushButton(Calculator)
        self.PlusMinus.setGeometry(QtCore.QRect(450, 230, 101, 91))

        font = QtGui.QFont()
        font.setFamily("STIX")
        font.setPointSize(24)

        self.PlusMinus.setFont(font)
        self.PlusMinus.setObjectName("PlusMinus")
        self.PlusMinus.setStyleSheet(stylesheet1)

        self.Equal = QtWidgets.QPushButton(Calculator)
        self.Equal.setGeometry(QtCore.QRect(230, 430, 101, 91))

        font = QtGui.QFont()
        font.setFamily("STIX")
        font.setPointSize(24)

        self.Equal.setFont(font)
        self.Equal.setObjectName("Equal")
        self.Equal.setStyleSheet(stylesheet1)

        self.Zero = QtWidgets.QPushButton(Calculator)
        self.Zero.setGeometry(QtCore.QRect(10, 430, 101, 91))
        
        font = QtGui.QFont()
        font.setFamily("STIX")
        font.setPointSize(24)

        self.Zero.setFont(font)
        self.Zero.setObjectName("Zero")

        self.C = QtWidgets.QPushButton(Calculator)
        self.C.setEnabled(True)
        self.C.setGeometry(QtCore.QRect(450, 330, 101, 91))

        font = QtGui.QFont()
        font.setFamily("STIX")
        font.setPointSize(24)

        self.C.setFont(font)
        self.C.setObjectName("C")
        self.C.setStyleSheet(stylesheet1)

        self.Exit = QtWidgets.QPushButton(Calculator)
        self.Exit.setEnabled(True)
        self.Exit.setGeometry(QtCore.QRect(450, 430, 101, 91))

        font = QtGui.QFont()
        font.setFamily("STIX")
        font.setPointSize(24)

        self.Exit.setFont(font)
        self.Exit.setObjectName("C")
        self.Exit.setStyleSheet(stylesheet2)

        self.Nine = QtWidgets.QPushButton(Calculator)
        self.Nine.setGeometry(QtCore.QRect(230, 130, 101, 91))

        font = QtGui.QFont()
        font.setFamily("STIX")
        font.setPointSize(24)

        self.Nine.setFont(font)
        self.Nine.setObjectName("Nine")

        self.Minus = QtWidgets.QPushButton(Calculator)
        self.Minus.setGeometry(QtCore.QRect(340, 330, 101, 91))

        font = QtGui.QFont()
        font.setFamily("STIX")
        font.setPointSize(24)

        self.Minus.setFont(font)
        self.Minus.setCheckable(False)
        self.Minus.setObjectName("Minus")
        self.Minus.setStyleSheet(stylesheet1)

        self.Three = QtWidgets.QPushButton(Calculator)
        self.Three.setGeometry(QtCore.QRect(230, 330, 101, 91))

        font = QtGui.QFont()
        font.setFamily("STIX")
        font.setPointSize(24)

        self.Three.setFont(font)
        self.Three.setObjectName("Three")

        self.One = QtWidgets.QPushButton(Calculator)
        self.One.setGeometry(QtCore.QRect(10, 330, 101, 91))

        font = QtGui.QFont()
        font.setFamily("STIX")
        font.setPointSize(24)

        self.One.setFont(font)
        self.One.setObjectName("One")

        self.Four = QtWidgets.QPushButton(Calculator)
        self.Four.setGeometry(QtCore.QRect(10, 230, 101, 91))

        font = QtGui.QFont()
        font.setFamily("STIX")
        font.setPointSize(24)

        self.Four.setFont(font)
        self.Four.setObjectName("Four")

        self.NumberField = QtWidgets.QLCDNumber(Calculator)
        self.NumberField.setGeometry(QtCore.QRect(13, 10, 531, 111))
        self.NumberField.setSmallDecimalPoint(False)
        self.NumberField.setDigitCount(16)
        self.NumberField.setObjectName("NumberField")
        self.NumberField.setStyleSheet("color: white; border: none; border-bottom: 1px solid rgb(58,61,76);")

        self.Plus = QtWidgets.QPushButton(Calculator)
        self.Plus.setGeometry(QtCore.QRect(340, 430, 101, 91))

        font = QtGui.QFont()
        font.setFamily("STIX")
        font.setPointSize(24)

        self.Plus.setFont(font)
        self.Plus.setObjectName("Plus")
        self.Plus.setStyleSheet(stylesheet1)

        self.Two = QtWidgets.QPushButton(Calculator)
        self.Two.setGeometry(QtCore.QRect(120, 330, 101, 91))

        font = QtGui.QFont()
        font.setFamily("STIX")
        font.setPointSize(24)

        self.Two.setFont(font)
        self.Two.setObjectName("Two")

        self.Back = QtWidgets.QPushButton(Calculator)
        self.Back.setGeometry(QtCore.QRect(450, 130, 101, 91))

        font = QtGui.QFont()
        font.setFamily("STIX")
        font.setPointSize(36)
        self.Back.setFont(font)
        
        self.Back.setObjectName("Back")
        self.Back.setStyleSheet(stylesheet1)

        self.retranslateUi(Calculator)
        QtCore.QMetaObject.connectSlotsByName(Calculator)

    def retranslateUi(self, Calculator):
        _translate = QtCore.QCoreApplication.translate
        Calculator.setWindowTitle(_translate("Calculator", "Calculator"))
        self.Five.setText(_translate("Calculator", "5"))
        self.Six.setText(_translate("Calculator", "6"))
        self.Seven.setText(_translate("Calculator", "7"))
        #self.Sqrt.setText(_translate("Calculator", "√"))
        self.Multiply.setText(_translate("Calculator", "*"))
        self.Decimal.setText(_translate("Calculator", "."))
        self.Eight.setText(_translate("Calculator", "8"))
        self.Divide.setText(_translate("Calculator", "÷"))
        self.PlusMinus.setText(_translate("Calculator", "±"))
        self.Equal.setText(_translate("Calculator", "="))
        self.Zero.setText(_translate("Calculator", "0"))
        self.C.setText(_translate("Calculator", "C"))
        self.Exit.setText(_translate("Calculator", "Exit"))
        self.Nine.setText(_translate("Calculator", "9"))
        self.Minus.setText(_translate("Calculator", "-"))
        self.Three.setText(_translate("Calculator", "3"))
        self.One.setText(_translate("Calculator", "1"))
        self.Four.setText(_translate("Calculator", "4"))
        self.Plus.setText(_translate("Calculator", "+"))
        self.Two.setText(_translate("Calculator", "2"))
        self.Back.setText(_translate("Calculator", "←"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Calculator = QtWidgets.QDialog()
    ui = Ui_Calculator()
    ui.setupUi(Calculator)
    Calculator.show()
    sys.exit(app.exec_())

