import sys
from os.path import basename
from PyQt5.QtCore import QPoint, Qt, QRect
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication, QPushButton, QMenu, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QHBoxLayout, QPushButton

class Box(QtWidgets.QWidget):
    title = "box"
    # numpy_image is the desired image we want to display given as a numpy array.
    def __init__(self, x,y,w,h):
        super(Box, self).__init__()
        self.x = x
        self.y = y
        self.w = w 
        self.h = h
        self.title = Box.title
        start_position = (self.x, self.y, self.w, self.h)


        # self.toolbar = self.addToolBar('Exit')

        self.setGeometry(*start_position)
        width = self.w - self.x
        height = self.h - self.y
        self.resize(width, height)

        tb = QtWidgets.QToolBar


        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        layout = QtWidgets.QHBoxLayout(self)

        # layout.addWidget(QtWidgets.QPushButton("TEST"))


        # self.setWindowFlags()

        self.setAttribute(Qt.WA_TranslucentBackground)
        frame =QFrame(self)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setLineWidth(0.6)

        layout.addWidget(frame)
        self.show()
    
    def close_window(self):
        self.close()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     mainMenu = Box()
#     sys.exit(app.exec_())
