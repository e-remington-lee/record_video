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

# animation group https://doc.qt.io/qt-5/qanimationgroup.html

class A3(QtWidgets.QWidget):
    def __init__(self, picture):
        super(A3, self).__init__()
        self.layout = QtWidgets.QHBoxLayout()
        self.pic_layout = QtWidgets.QHBoxLayout()
        self.picture = picture

        # self.label1 = QtWidgets.QLabel(self)
        # self.label1.setPixmap(QtGui.QPixmap("reluu_application\\GUI_improvements\\master_pyqt5\\active_user_talk_bubble.png"))
        # self.label1.setScaledContents(True)
        # self.pic_layout.addWidget(self.label)

        # self.label2 = QtWidgets.QLabel(self)
        # self.label2.setPixmap(QtGui.QPixmap("reluu_application\\GUI_improvements\\master_pyqt5\\active_caller_talk_bubble.png"))
        # self.label2.hide()
        # self.label2.setScaledContents(True)
        # self.pic_layout.addWidget(self.label)

        self.button = QtWidgets.QPushButton("start pink", clicked=self.start_timer)
        self.button2 = QtWidgets.QPushButton("start green", clicked=self.start_animation2)
        self.button3 = QtWidgets.QPushButton("stop timer", clicked=self.reset)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)

        self.layout.addLayout(self.pic_layout)
        self.setLayout(self.layout)
        self.setGeometry(1000,500,400,600)

        self.caller_label1 = QtWidgets.QLabel(self)
        self.caller_label2 = QtWidgets.QLabel(self)
        self.caller_label3 = QtWidgets.QLabel(self)

        self.caller_label1_bool = True
        self.caller_label2_bool = False
        self.caller_label3_bool = False

        self.a1, self.a2 = 1,1
        self.b1, self.b2 = 3,3

        self.pnt11, self.pnt12 = 100,100
        self.pnt21, self.pnt22 = 99,99

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.start_animation1)
        # self.timer.start()

    
    def start_timer(self):
        self.timer.start()

    def start_animation1(self):
        if self.caller_label1_bool:
            self.animate_bubble(self.caller_label1, self.caller_label1_bool, self.caller_label2, self.caller_label2_bool)
        elif self.caller_label2_bool:
            self.animate_bubble(self.caller_label2, self.caller_label1_bool, self.caller_label2, self.caller_label2_bool)
        elif self.caller_label3_bool:
            self.animate_bubble(self.caller_label3, self.caller_label1_bool, self.caller_label2, self.caller_label2_bool)
    
    
    def animate_bubble(self, label, label_bool, next_label, next_label_bool):
        if self.caller_label1_bool:
            self.caller_label1.hide()
        elif self.caller_label2_bool:
            self.caller_label2.hide()
        elif self.caller_label3_bool:
            self.caller_label3.hide()
        label.setPixmap(QtGui.QPixmap(self.picture))
        label.setScaledContents(True)
        start_pnt = QtCore.QPoint(self.pnt11, self.pnt12)
        end_ptn = QtCore.QPoint(self.pnt21, self.pnt22)
        start_size = QtCore.QSize(self.a1,self.a2)
        end_size = QtCore.QSize(self.b1, self.b2)
        anim = QtCore.QPropertyAnimation(label, b"geometry")
        anim.setDuration(50)
        anim.setStartValue(QtCore.QRect(start_pnt, start_size))
        anim.setEndValue(QtCore.QRect(end_ptn, end_size))
        anim.start()
        self.increase(label, label_bool, next_label, next_label_bool)
    

    def increase(self, label, label_bool, next_label, next_label_bool):
        self.a1, self.a2 = self.b1, self.b2
        self.b1 += 2
        self.b2 += 2
        self.pnt11, self.pnt12 = self.pnt21, self.pnt22
        self.pnt21 -=1
        self.pnt22 -=1
        if self.caller_label1_bool:
            self.caller_label1.show()
        elif self.caller_label2_bool:
            self.caller_label2.show()
        elif self.caller_label3_bool:
            self.caller_label3.show()
        self.check_size(label, label_bool, next_label, next_label_bool)

        
    def check_size(self, label, label_bool, next_label, next_label_bool):
        if self.b1 > 65:
            self.a1, self.a2 = 1,1
            self.b1, self.b2 = 3,3
            if self.caller_label1_bool:
                self.caller_label1_bool, self.caller_label2_bool = False, True
                self.pnt11, self.pnt12 = 100,180
                self.pnt21, self.pnt22 = 99,179
            elif self.caller_label2_bool:
                self.caller_label2_bool, self.caller_label3_bool = False, True
                self.pnt11, self.pnt12 = 100,260
                self.pnt21, self.pnt22 = 99,259
            elif self.caller_label3_bool:
                self.caller_label3_bool, self.caller_label1_bool = False, True
                self.pnt11, self.pnt12 = 100,100
                self.pnt21, self.pnt22 = 99,99


    def reset(self):
        self.timer.stop()


    def start_animation2(self):
        self.anim2 = QtCore.QPropertyAnimation(self.label2, b"geometry")
        self.anim2.setDuration(3000)
        self.anim2.setStartValue(QtCore.QRect(300, 100, 5, 5))
        self.anim2.setEndValue(QtCore.QRect(275, 75, 65, 65))
        self.label2.show()
        self.anim2.start()


if __name__ == "__main__":
    q = QtWidgets.QApplication()
    a = A3("reluu_application\\GUI_improvements\\master_pyqt5\\active_user_talk_bubble.png")
    a.show()
    sys.exit(q.exec_())
