import sys
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
# from PySide2 import uic

## Widgets can only be added to other widgets or layouts
class MainWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        email_label = QtWidgets.QLabel("Email")
        password_label = QtWidgets.QLabel("Password")

        email_input = QtWidgets.QLineEdit()
        email_input.setPlaceholderText("Enter email here")
        password_input = QtWidgets.QLineEdit()
        password_input.setPlaceholderText("Enter password here")
        password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        cancel_button = QtWidgets.QPushButton("Canel")
        submit_button = QtWidgets.QPushButton("Login")

        # self.layout = QtWidgets.QVBoxLayout()
        # self.layout = QtWidgets.QGridLayout()
        # self.layout.addWidget(email_label, 0, 0)
        # self.layout.addWidget(email_input, 1, 0)
        # self.layout.addWidget(password_label, 2, 0)
        # self.layout.addWidget(password_input, 3, 0)

        self.layout = QtWidgets.QFormLayout()
        self.layout.addRow("Email", email_input)
        self.layout.addRow("Password", password_input)

        abl = QtWidgets.QWidget()
        abl.setLayout(QtWidgets.QHBoxLayout())
        abl.layout().addWidget(cancel_button)
        abl.layout().addWidget(submit_button)
        # self.layout.addLayout(action_button_layout)
        self.layout.addRow("", abl)
        self.setLayout(self.layout)

        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())