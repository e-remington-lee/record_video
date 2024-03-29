import os
import sys
import importlib.util

print('Importing local shiboken2')
abspath = os.path.dirname(os.path.abspath(sys.argv[0]))
MODULE_PATH2 = "./shiboken2/__init__.py"
MODULE_PATH2_ABS = os.path.join(abspath, "./shiboken2/__init__.py")
MODULE_NAME2 = "shiboken2"

spec2 = importlib.util.spec_from_file_location(MODULE_NAME2, MODULE_PATH2_ABS)
shiboken2 = importlib.util.module_from_spec(spec2)
sys.modules[spec2.name] = shiboken2
spec2.loader.exec_module(shiboken2)
print(shiboken2.__version__)

print('Importing local PySide2')
MODULE_PATH = "./PySide2/__init__.py"
MODULE_PATH_ABS = os.path.join(abspath, "./PySide2/__init__.py")
MODULE_NAME = "PySide2"

spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH_ABS)
PySide2 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = PySide2
spec.loader.exec_module(PySide2)
print(PySide2.__version__)

import numpy as np
from PIL import ImageGrab
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt
import pyautogui

import Reluu
import running_model_v2

class GrabImage(QtWidgets.QWidget):
    is_snipping = False
    background = True

    def __init__(self):
        super(GrabImage, self).__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        width, height = pyautogui.size()
        self.setGeometry(0, 0, width, height)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.x11 = None
        self.y11 = None
        self.x22 = None
        self.y22 = None
        icon = QtGui.QIcon("reluu_gui\\auxiliary_files\\logo_transparent_background.png")
        self.setWindowIcon(icon)

    def start_grab(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        GrabImage.background = False
        GrabImage.is_snipping = True
        self.setWindowOpacity(0.2)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.show()

    def paintEvent(self, event):
        if GrabImage.is_snipping:
            brush_color = (128, 128, 255, 100)
            lw = 3
            opacity = 0.3
        else:
            # reset points, so the rectangle won't show up again.
            self.begin = QtCore.QPoint()
            self.end = QtCore.QPoint()
            brush_color = (0, 0, 0, 0)
            lw = 0
            opacity = 0

        self.setWindowOpacity(opacity)
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), lw))
        qp.setBrush(QtGui.QColor(*brush_color))
        rect = QtCore.QRectF(self.begin, self.end)
        qp.drawRect(rect)

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()
        self.x11, self.y11 = pyautogui.position()


    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()
        self.x22, self.y22 = pyautogui.position()

    def mouseReleaseEvent(self, event):
        GrabImage.is_snipping = False
        QtWidgets.QApplication.restoreOverrideCursor()
        # x1 = min(self.begin.x(), self.end.x())
        # y1 = min(self.begin.y(), self.end.y())
        # x2 = max(self.begin.x(), self.end.x())
        # y2 = max(self.begin.y(), self.end.y())
        x1 = min(self.x11, self.x22)
        y1 = min(self.y11, self.y22)
        x2 = max(self.x11, self.x22)
        y2 = max(self.y11, self.y22)


        print(self.x11, self.y11, self.x22, self.y22)
        self.repaint()
        QtWidgets.QApplication.processEvents()
        self.close()
        # width = self.x22 - self.x11
        # height = self.y22 - self.y11
        # We put absolute cordinates here bc Pillow uses absolute cordinates
        self.model_window = running_model_v2.ActiveModelWindow(self.x11, self.y11, self.x22, self.y22)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    abc = GrabImage()
    abc.start_grab()
    sys.exit(app.exec_())