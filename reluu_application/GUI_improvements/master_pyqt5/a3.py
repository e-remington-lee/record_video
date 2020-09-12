import sys
from PySide2 import QtWidgets, QtGui, QtCore, QtCharts

# https://www.learnpyqt.com/courses/custom-widgets/bitmap-graphics/
# https://www.learnpyqt.com/courses/custom-widgets/creating-your-own-custom-widgets/

# Key animation step
# https://www.youtube.com/watch?v=xewHDkCKVoQ

# Bring widget to front
# https://stackoverflow.com/questions/3821743/how-to-bring-the-widget-bring-to-front-in-qt

# Animated circle enlarging
# https://stackoverflow.com/questions/50550089/qt-animating-qpixmap

class A3(QtWidgets.QWidget):
    def __init__(self):
        super(A3, self).__init__()
        self.layout = QtWidgets.QHBoxLayout()
        self.pic_layout = QtWidgets.QHBoxLayout()

        self.label1 = QtWidgets.QLabel(self)
        self.label1.setPixmap(QtGui.QPixmap("reluu_application\\GUI_improvements\\master_pyqt5\\active_user_talk_bubble.png"))
        self.label1.hide()
        self.label1.setScaledContents(True)
        # self.pic_layout.addWidget(self.label)

        self.label2 = QtWidgets.QLabel(self)
        self.label2.setPixmap(QtGui.QPixmap("reluu_application\\GUI_improvements\\master_pyqt5\\active_caller_talk_bubble.png"))
        self.label2.hide()
        self.label2.setScaledContents(True)
        # self.pic_layout.addWidget(self.label)

        self.button = QtWidgets.QPushButton("start pink", clicked=self.start_animation1)
        self.button2 = QtWidgets.QPushButton("start green", clicked=self.start_animation2)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.button2)

        self.layout.addLayout(self.pic_layout)
        self.setLayout(self.layout)
        self.setGeometry(1000,1000,400,400)
    
    # def increase
    
    def start_animation1(self):
        pnt = QtCore.QPoint(100,100)
        sz = QtCore.QSize(5,5)
        self.anim = QtCore.QPropertyAnimation(self.label1, b"geometry")
        self.anim.setDuration(3000)
        self.anim.setStartValue(QtCore.QRect(pnt, sz))
        self.anim.setEndValue(QtCore.QRect(75, 75, 65, 65))
        self.label1.show()
        self.anim.start()

    def start_animation2(self):
        self.anim = QtCore.QPropertyAnimation(self.label2, b"geometry")
        self.anim.setDuration(3000)
        self.anim.setStartValue(QtCore.QRect(300, 100, 5, 5))
        self.anim.setEndValue(QtCore.QRect(275, 75, 65, 65))
        self.label2.show()
        self.anim.start()


if __name__ == "__main__":
    q = QtWidgets.QApplication()
    a = A3()
    a.show()
    sys.exit(q.exec_())
