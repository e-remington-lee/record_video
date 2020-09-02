import sys
from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QDesktopWidget
from PySide2.QtGui import QIcon, QPixmap

class LoginWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(LoginWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("ReLuu")
        self.resize(470,378)
        self.setStyleSheet("background-color: #f3fcff;")
        self.show_logo()


    def show_logo(self):
        # self.logo_widget = QWidget(self)
        # self.logo_widget.setGeometry(50,50,100,100)
        self.logo = QLabel(self)
        # self.logo.setPixmap(QPixmap("logo_transparent_background.png"))
        self.logo.setPixmap(QPixmap("white_logo_color_background.png"))
        self.logo.setScaledContents(True)
        # self.label.resize(100, 100)
        # self.setCentralWidget(self.label)


        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    app.exec_()