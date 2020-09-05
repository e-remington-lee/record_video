import sys
# from PySide2.QtWidgets import QApplication, QSizePolicy, QVBoxLayout, QGridLayout, QWidget, QMainWindow, QLabel
# from PySide2.QtGui import QIcon, QPixmap
# from PySide2.QtCore import QRect, Qt
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
from login_menu_ui import Ui_MainWindow

class LoginWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(LoginWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)
        icon = QtGui.QIcon("reluu_application/GUI_improvements/logo_transparent_background.png")
        self.setWindowIcon(icon)
        self.Sign_in_button.clicked.connect(self.gogo)

    def gogo(self):
        print("fuckyeah")

        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    app.exec_()
