from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys

from functools import partial

from Config import _App
DEFAULT_LABEL_STRING = "Enter your name"

class KeyboardWidget(QtWidgets.QDialog):
    def __init__(self, MainWindow):
        super(KeyboardWidget, self).__init__()
        uic.loadUi('keyboardwidget.ui', self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WA_ShowWithoutActivating)
        self.setModal(True)

        self.MainWindow = MainWindow
        self.key_buttons = []
        self.fkey_buttons = []

        self.key_list = [
            [ '`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 
            'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '\\',
            'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'",
            'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', ' ', '.com' ],

            [ '`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '\\',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', "'",
            'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', ' ', '.COM' ],

            [ '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', 
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '|',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"',
            'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?', ' ', '.COM' ],

            [ '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', 
            'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '|',
            'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ':', '"',
            'z', 'x', 'c', 'v', 'b', 'n', 'm', '<', '>', '?', ' ', '.com' ]
        ]

        self.fkey_list = [
            QtCore.Qt.Key_Tab,
            QtCore.Qt.Key_Home,
            QtCore.Qt.Key_End,
            QtCore.Qt.Key_Left,
            QtCore.Qt.Key_Right,
            QtCore.Qt.Key_Up,
            QtCore.Qt.Key_Down,
            QtCore.Qt.Key_Backspace,
            QtCore.Qt.Key_Delete,
            QtCore.Qt.Key_Return

        ]

        self.initKeyboard()
        self.initConnections()

    def initKeyboard(self, Src = None, LabelText = DEFAULT_LABEL_STRING, EchoMode = QtWidgets.QLineEdit.Normal):
        self.Capslock = 0b00
        self.Shift = 0b00
        self.key_capslock.setChecked(False)
        self.key_shift.setChecked(False)

        self.Label.setText(LabelText)
        self.lineEdit.setEchoMode(EchoMode)
        self.source = _App.KEYBOARD_TEXT

        if Src is None:
            self.lineEdit.setText("")
        else:
            self.lineEdit.setText(Src)
    
    def showEvent(self, event):
        self.lineEdit.deselect()
        self.lineEdit.setCursorPosition(9999)
        #self.lineEdit.selectAll()
        #self.lineEdit.setText("")

    def initConnections(self):
        # char key buttons
        self.key_buttons.append(self.key_accent)
        self.key_buttons.append(self.key_1)
        self.key_buttons.append(self.key_2)
        self.key_buttons.append(self.key_3)
        self.key_buttons.append(self.key_4)
        self.key_buttons.append(self.key_5)
        self.key_buttons.append(self.key_6)
        self.key_buttons.append(self.key_7)
        self.key_buttons.append(self.key_8)
        self.key_buttons.append(self.key_9)
        self.key_buttons.append(self.key_0)
        self.key_buttons.append(self.key_minus)
        self.key_buttons.append(self.key_equal)
        self.key_buttons.append(self.key_q)
        self.key_buttons.append(self.key_w)
        self.key_buttons.append(self.key_e)
        self.key_buttons.append(self.key_r)
        self.key_buttons.append(self.key_t)
        self.key_buttons.append(self.key_y)
        self.key_buttons.append(self.key_u)
        self.key_buttons.append(self.key_i)
        self.key_buttons.append(self.key_o)
        self.key_buttons.append(self.key_p)
        self.key_buttons.append(self.key_backslash)
        self.key_buttons.append(self.key_a)
        self.key_buttons.append(self.key_s)
        self.key_buttons.append(self.key_d)
        self.key_buttons.append(self.key_f)
        self.key_buttons.append(self.key_g)
        self.key_buttons.append(self.key_h)
        self.key_buttons.append(self.key_j)
        self.key_buttons.append(self.key_k)
        self.key_buttons.append(self.key_l)
        self.key_buttons.append(self.key_semicolon)
        self.key_buttons.append(self.key_apos)
        self.key_buttons.append(self.key_z)
        self.key_buttons.append(self.key_x)
        self.key_buttons.append(self.key_c)
        self.key_buttons.append(self.key_v)
        self.key_buttons.append(self.key_b)
        self.key_buttons.append(self.key_n)
        self.key_buttons.append(self.key_m)
        self.key_buttons.append(self.key_comma)
        self.key_buttons.append(self.key_fullstop)
        self.key_buttons.append(self.key_slash)
        self.key_buttons.append(self.key_space)
        self.key_buttons.append(self.key_dotcom)

        for x in range(47):
            self.key_buttons[x].clicked.connect(partial(self.key_pressed, x))


        # function key buttons
        self.fkey_buttons.append(self.key_tab)
        self.fkey_buttons.append(self.key_home)
        self.fkey_buttons.append(self.key_end)
        self.fkey_buttons.append(self.key_left)
        self.fkey_buttons.append(self.key_right)
        self.fkey_buttons.append(self.key_up)
        self.fkey_buttons.append(self.key_down)
        self.fkey_buttons.append(self.key_backspace)
        self.fkey_buttons.append(self.key_delete)
        self.fkey_buttons.append(self.key_enter)

        for x in range(10):
            self.fkey_buttons[x].clicked.connect(partial(self.fkey_pressed, x))

        # modifier buttons
        self.key_capslock.clicked.connect(self.caps_pressed)
        self.key_shift.clicked.connect(self.shift_pressed)
        self.key_clear.clicked.connect(self.clear_pressed)

        # accept & reject buttons
        self.key_accept.clicked.connect(self.accept_pressed)
        self.key_reject.clicked.connect(self.reject_pressed)

        self.lineEdit.returnPressed.connect(self.accept_pressed)

    def key_pressed(self, index):
        key_to_add = self.key_list[self.Capslock | self.Shift][index]
        eventPress = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, 0, QtCore.Qt.NoModifier, key_to_add)
        QtCore.QCoreApplication.postEvent(self.lineEdit, eventPress)
        #eventRelease = QtGui.QKeyEvent(QtCore.QEvent.KeyRelease, 0, QtCore.Qt.NoModifier, key_to_add)
        #QtCore.QCoreApplication.postEvent(self.lineEdit, eventRelease)

        if self.key_shift.isChecked():
            self.Shift = 0b00
            self.key_shift.setChecked(False)

    def fkey_pressed(self, index):
        self._key_press(self.fkey_list[index])
    
    def _key_press(self, key):
        event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, key, QtCore.Qt.NoModifier)
        QtCore.QCoreApplication.postEvent(self.lineEdit, event)

    def caps_pressed(self):
        if self.key_capslock.isChecked():
            self.Capslock = 0b01
        else:
            self.Capslock = 0b00
    
    def shift_pressed(self):
        if self.key_shift.isChecked():
            self.Shift = 0b10
        else:
            self.Shift = 0b00

    def clear_pressed(self):
        self.Capslock = 0b00
        self.Shift = 0b00
        self.key_capslock.setChecked(False)
        self.key_shift.setChecked(False)

        self.lineEdit.setText("")

    def accept_pressed(self):
        self.source[0] = self.lineEdit.text()
        return self.accept()

    def reject_pressed(self):
        self.reject()

