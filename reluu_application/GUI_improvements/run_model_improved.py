import sys
from threading import Lock
from multiprocessing import Process, Queue

import numpy as np
from PySide2 import QtWidgets, QtGui, QtCore, QtCharts

import login_menu
import image_box_movable

class RunModelWindow(QtWidgets.QWidget):
    image_box = None

    def __init__(self, start_box_x1, start_box_y1, start_box_x2, start_box_y2):
        super(RunModelWindow, self).__init__()
        self.inputs_queue, self.outputs_queue = Queue(), Queue()
        self.update_position_lock = Lock()
        self.image_box = image_box_movable.ImageBox(start_box_x1, start_box_y1, start_box_x2, start_box_y2, 
                                                    self.inputs_queue, self.update_position_lock)

        self.b1 = QtWidgets.QPushButton()
        self.b1.setText("hello!!")
        self.b1.clicked.connect(self.close_all)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.b1)
        self.setLayout(self.layout)
        self.show()

    def close_all(self):
        self.image_box.close()
        self.close()
        self.login_menu_2 = login_menu.MainMenu()
        self.login_menu_2.show()

    def closeEvent(self, event):
        self.image_box.close()
        self.close()



