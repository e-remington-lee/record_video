import sys
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
from login_menu_qtd import Ui_MainWindow

class LoginWindow(QtWidgets.QWidget, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(LoginWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        icon = QtGui.QIcon("reluu_application/GUI_improvements/logo_transparent_background.png")
        self.setWindowIcon(icon)
    
        self.Sign_in_button.clicked.connect(lambda: self.sign_in_1(self.email_input.text(), self.password_input.text()))

    def sign_in_1(self, email, password):
        if email == "1" and password == "1":
            if self.keep_signed_in.isChecked():
                print("staying signed in")
            self.close()
            self.main_menu = MainMenu()
            self.main_menu.show()
        else: 
            print("failed to login")


class MainMenu(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainMenu, self).__init__(*args, **kwargs)

        self.start_model_button = QtWidgets.QPushButton()
        self.start_model_button.setText("Start")
        self.start_model_button.clicked.connect(self.start_model)

        self.logout_button = QtWidgets.QPushButton()
        self.logout_button.setText("Logout")
        self.logout_button.clicked.connect(self.logout)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.start_model_button)
        self.layout.addWidget(self.logout_button)
        self.setLayout(self.layout)

    def start_model(self):
        print("starting model")
    
    def logout(self):
        self.close()
        self.login = LoginWindow()
        self.login.show()

        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
