import sys
from os.path import basename
from PySide2.QtCore import QPoint, Qt, QRect
from PySide2.QtWidgets import QTabWidget, QWidget, QAction, QMainWindow, QApplication, QVBoxLayout, QPushButton, QMenu, QFileDialog, QWidget, QFrame, QHBoxLayout
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
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        tab = QWidget()
        tab.setAttribute(Qt.WA_OpaquePaintEvent)

        tw = QTabWidget()
        tw.addTab(tab, "example")
        
        # tw.setStyleSheet("QTabBar::tab { background: transparent; }")

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(tw)
        self.show()

    def close_window(self):
        self.close()
