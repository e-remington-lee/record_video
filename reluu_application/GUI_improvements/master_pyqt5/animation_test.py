import sys
from PySide2 import QtWidgets, QtGui, QtCore, QtCharts


class RMW(QtWidgets.QWidget):
    def __init__(self):
        super(RMW, self).__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.ball_layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel()
        cv = QtGui.QPixmap(500,500)
        cv.fill(QtGui.QColor(150,200,60, 255))

        self.label.setPixmap(cv)

        painter = QtGui.QPainter(self.label.pixmap())

        painter.setPen(QtGui.QPen(QtCore.Qt.green,  8, QtCore.Qt.SolidLine))

        painter.setBrush(QtGui.QBrush(QtCore.Qt.red, QtCore.Qt.SolidPattern))

        painter.drawEllipse(40, 40, 400, 400)
        painter.end()
        b2 = QtWidgets.QPushButton("Push!", clicked=self.push)
        self.ball_layout.addWidget(self.label)
        self.ball_layout.addWidget(b2)

        self.button_layout = QtWidgets.QHBoxLayout()
        b1 = QtWidgets.QPushButton("Push!", clicked=self.push)
        self.button_layout.addWidget(b1)

        self.layout.addLayout(self.ball_layout)
        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)
        self.show()
    

    def push(self):
        cv = QtGui.QPixmap(50,50)
        
        cv.fill(QtGui.QColor(0,0,255, 255))
        self.label.setPixmap(cv)
        print("push button")



if __name__ == "__main__":
    app = QtWidgets.QApplication()
    abc = RMW()
    sys.exit(app.exec_())