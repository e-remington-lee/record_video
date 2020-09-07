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

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(email_label)
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.submit_button)

        # self.layout = QtWidgets.QFormLayout()
        # self.layout.addRow("Email", self.email_input)
        # self.layout.addRow("Password", self.password_input)

        # abl = QtWidgets.QWidget()
        # abl.setLayout(QtWidgets.QHBoxLayout())
        # abl.layout().addWidget(self.cancel_button)
        # abl.layout().addWidget(self.submit_button)
        # # self.layout.addLayout(action_button_layout)
        # self.layout.addRow("", abl)
        self.setLayout(self.layout)

        self.cancel_button.clicked.connect(self.close)
        self.submit_button.clicked.connect(self.authenticate)

        self.email_input.textChanged.connect(self.set_button_text)
        self.show()


    def set_button_text(self, text): 
        if text:
            self.submit_button.setText(f'Login {text}')
        else:
            self.submit_button.setText(f'Login')


    def authenticate(self):
        em = "1234"
        pw = "1234"

        print(self.email_input.text(), self.password_input.text())
        # if self.email_input.text() == em and self.password_input.text() == pw:
        #     QtWidgets.QMessageBox.information(self, "Success!", "win!")
        # else:
        #     QtWidgets.QMessageBox.critical(self, "Error", "login failed")

        abc = MainMenu()
        abc.show()
        
class MainMenu(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.resize(640, 480)
        self.message_a_edit = QtWidgets.QLineEdit()
        self.message_b_edit = QtWidgets.QLineEdit()
        self.cancel_button = QtWidgets.QPushButton('Cancel')
        self.submit_button = QtWidgets.QPushButton('Submit')

        self.setLayout(QtWidgets.QFormLayout())
        self.layout().addRow('Message A', self.message_a_edit)
        self.layout().addRow('Message B', self.message_b_edit)
        buttons = QtWidgets.QWidget()
        buttons.setLayout(QtWidgets.QHBoxLayout())
        buttons.layout().addWidget(self.cancel_button)
        buttons.layout().addWidget(self.submit_button)
        self.layout().addRow('', buttons)

        self.submit_button.clicked.connect(self.on_submit)
        self.cancel_button.clicked.connect(self.close)

    def set_messages(self, message_a, message_b):

        self.message_a_edit.setText(message_a)
        self.message_b_edit.setText(message_b)

    def on_submit(self):
        self.submitted.emit(
            self.message_a_edit.text(),
            self.message_b_edit.text()
            )
        self.close()
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     self.start_model_button = QtWidgets.QPushButton()
    #     self.start_model_button.setText("Start")
    #     self.start_model_button.clicked.connect(self.start_model)

    #     self.logout_button = QtWidgets.QPushButton()
    #     self.logout_button.setText("Logout")
    #     self.logout_button.clicked.connect(self.logout)

    #     self.layout = QtWidgets.QVBoxLayout()
    #     self.layout.addWidget(self.start_model_button)
    #     self.layout.addWidget(self.logout_button)
    #     self.setLayout(self.layout)

    # def start_model(self):
    #     print("starting model")
    
    # def logout(self):
    #     self.close()
    #     login = LoginWindow()
    #     login.show()
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())