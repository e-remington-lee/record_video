import tkinter as tk
import numpy as np
import cv2
from PIL import ImageGrab
from PySide2 import QtWidgets, QtCore, QtGui
import faceReader_gui
from PySide2.QtCore import Qt

# Testing
import pyautogui

class SnippingWidget(QtWidgets.QWidget):
    is_snipping = False
    background = True

    def __init__(self, parent=None):
        super(SnippingWidget, self).__init__()
        self.parent = parent
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.x11 = None
        self.y11 = None
        self.x22 = None
        self.y22 = None

    def start(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        SnippingWidget.background = False
        SnippingWidget.is_snipping = True
        self.setWindowOpacity(0.2)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.show()

    def paintEvent(self, event):
        if SnippingWidget.is_snipping:
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
        # print(pyautogui.position())

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()
        self.x22, self.y22 = pyautogui.position()

    def mouseReleaseEvent(self, event):
        SnippingWidget.is_snipping = False
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
        # QtWidgets.QApplication.processEvents()
        self.parent._Menu__create_box(x1, y1, x2, y2)
        self.close()
        

