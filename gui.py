from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from emotion_detection_model import main, Faces


def main_2():
    Application()

def Application():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(500,500,500,500)
    window.setWindowTitle("ReLuu FaceNet")

    label = QtWidgets.QLabel(window)
    label.setText("Start Application")
    label.move(200,50)

    button = QtWidgets.QPushButton(window)
    button.setText("Run Model")
    button.move(200,100)
    button.clicked.connect(main)

    # button.setText("Stop Model")
    # button.move(200,150)
    # button.connect(Faces().stop())

    window.show()
    sys.exit(app.exec_())

main_2()
