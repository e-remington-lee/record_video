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

        self.email_input = QtWidgets.QLineEdit()
        self.email_input.setPlaceholderText("Enter email here")
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Enter password here")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        self.cancel_button = QtWidgets.QPushButton("Canel")
        self.submit_button = QtWidgets.QPushButton("Login")

        # self.layout = QtWidgets.QVBoxLayout()
        # self.layout = QtWidgets.QGridLayout()
        # self.layout.addWidget(email_label, 0, 0)
        # self.layout.addWidget(email_input, 1, 0)
        # self.layout.addWidget(password_label, 2, 0)
        # self.layout.addWidget(password_input, 3, 0)

        self.layout = QtWidgets.QFormLayout()
        self.layout.addRow("Email", self.email_input)
        self.layout.addRow("Password", self.password_input)

        abl = QtWidgets.QWidget()
        abl.setLayout(QtWidgets.QHBoxLayout())
        abl.layout().addWidget(self.cancel_button)
        abl.layout().addWidget(self.submit_button)
        # self.layout.addLayout(action_button_layout)
        self.layout.addRow("", abl)
        self.setLayout(self.layout)

        self.cancel_button.clicked.connect(self.close)
        self.submit_button.clicked.connect(self.authenticate)

        self.email_input.textChanged.connect(self.set_button_text)


    def set_button_text(self, text): 
        if text:
            self.submit_button.setText(f'Login {text}')
        else:
            self.submit_button.setText(f'Login')


    def authenticate(self):
        em = "1234"
        pw = "1234"

        print(self.email_input, self.password_input)
        if self.email_input.text() == em and self.password_input.text() == pw:
            QtWidgets.QMessageBox.information(self, "Success!", "win!")
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "login failed")
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())