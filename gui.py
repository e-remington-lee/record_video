from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import cv2.cv2 as cv2
from emotion_detection_model_5 import main


def start():
    Application()

def detect_faces(idk=None):
    # TODO remove the main() method in the detection_model you are importing
    print(idk)
    main()

def click_and_crop():
    # Will call the detect faces with the defined image
    # Figure out threading
    detect_faces()

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

    button.clicked.connect(detect_faces)

    button2 = QtWidgets.QPushButton(window)
    button2.setText("Draw Box")
    button2.move(200,150)
    button2.clicked.connect(click_and_crop)

    # button.setText("Stop Model")
    # button.move(200,150)
    # button.connect(Faces().stop())

    window.show()
    sys.exit(app.exec_())

start()