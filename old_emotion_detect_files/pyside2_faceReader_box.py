import sys
from os.path import basename
from PySide2.QtCore import QPoint, Qt, QRect
from PySide2.QtWidgets import QTabWidget, QWidget, QLayout, QAction, QMainWindow, QApplication, QVBoxLayout, QPushButton, QMenu, QFileDialog, QWidget, QFrame, QHBoxLayout
from PySide2.QtGui import QPixmap, QImage, QPainter, QPen

from PySide2 import QtWidgets, QtCore, QtGui

class Box(QWidget):
    title = "box"
    def __init__(self, x,y,w,h):
        QWidget.__init__(self)
        self.x = x
        self.y = y
        self.w = w 
        self.h = h
        self.title = Box.title
        start_position = (self.x, self.y, self.w, self.h)
        

        self.setGeometry(*start_position)
        width = self.w - self.x
        height = self.h - self.y
        self.resize(width, height)

        tb = QtWidgets.QToolBar

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QtWidgets.QHBoxLayout(self)
        frame = QFrame(self)
        # frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShape(QFrame.WinPanel)    
        frame.setLineWidth(.1)
        layout.addWidget(frame)

        self.show()

    def close_window(self):
        self.close()
