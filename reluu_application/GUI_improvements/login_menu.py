import sys
from PySide2.QtWidgets import QApplication, QSizePolicy, QVBoxLayout, QGridLayout, QWidget, QMainWindow, QLabel
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtCore import QRect, Qt

class LoginWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(LoginWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("ReLuu")
        self.layout = QGridLayout()
        self.resize(470,378)
        self.setStyleSheet("background-color: #f3fcff;")
        self.show_logo()
        self.setLayout(self.layout)

    def show_logo(self):
        logo = QLabel(self)
        logo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        logo.setAlignment(Qt.AlignCenter)
        img = QPixmap("reluu_application\\GUI_improvements\\logo_transparent_background.png")
        img2 = img.scaled(240,210)
        logo.setPixmap(img2)
        self.layout.addWidget(logo)


        # logo.show()

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    app.exec_()
