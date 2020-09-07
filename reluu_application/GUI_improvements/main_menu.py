import sys
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
from login_menu import LoginWindow

class MainMenu(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainMenu, self).__init__(*args, **kwargs)
        self.version = "1.0.0"

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
        login = LoginWindow()
        login.show()

        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainMenu()
    window.show()
    app.exec_()