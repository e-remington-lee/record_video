from PySide2.QtCore import Qt, QPoint
from PySide2.QtWidgets import QApplication, QFrame, QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QPushButton, QStyle, QSpinBox, QLabel
from PySide2.QtGui import QRegion

from multiprocessing import Queue

class VLine(QFrame):
    def __init__(self):
        QFrame.__init__(self)
        self.setFrameShape(self.VLine)
        self.setFrameStyle(self.Sunken)

class Grabber(QWidget):
    dirty = True
    def __init__(self, x, y, w, h, inputs_queue, update_position_queue, update_position_lock):
        QWidget.__init__(self)   
        self.setWindowTitle('ReLuu FaceReader')
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.inputs_queue = inputs_queue
        self.update_position_queue = update_position_queue
        self.update_position_lock = update_position_lock
        self.setGeometry(self.x, self.y, self.w, self.h)
        self.acceptDrops()
        # Window stays on top, and the other 2 combine to remove the min/close/expand buttons
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | Qt.WindowTitleHint)        
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        # limit widget AND layout margins
        layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # create a "placeholder" widget for the screen grab geometry
        self.grabWidget = QWidget()
        self.grabWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.grabWidget)
        self.show()

    def updateMask(self):
        # get the *whole* window geometry, including its titlebar and borders
        frameRect = self.frameGeometry()

        # get the grabWidget geometry and remap it to global coordinates
        grabGeometry = self.grabWidget.geometry()
        grabGeometry.moveTopLeft(self.grabWidget.mapToGlobal(QPoint(0, 0)))
        
        self.update_position_lock.acquire()
        #Sends info to the input queue
        x1 = grabGeometry.getRect()[0]
        y1 = grabGeometry.getRect()[1]
        width = grabGeometry.getRect()[2]
        height = grabGeometry.getRect()[3]
        message = f"UPDATE {x1} {y1} {width} {height}"
        if not self.update_position_queue.empty():
            _ = self.update_position_queue.get()
            self.update_position_queue.put(message)
        else:
            self.update_position_queue.put(message)
            
        self.inputs_queue.put(message)

        self.update_position_lock.release()
        
        # get the actual margins between the grabWidget and the window margins
        left = frameRect.left() - grabGeometry.left()
        top = frameRect.top() - grabGeometry.top()
        right = frameRect.right() - grabGeometry.right()
        bottom = frameRect.bottom() - grabGeometry.bottom()

        # reset the geometries to get "0-point" rectangles for the mask
        frameRect.moveTopLeft(QPoint(0, 0))
        grabGeometry.moveTopLeft(QPoint(0, 0))

        # create the base mask region, adjusted to the margins between the
        # grabWidget and the window as computed above
        region = QRegion(frameRect.adjusted(left, top, right, bottom))
        # "subtract" the grabWidget rectangle to get a mask that only contains
        # the window titlebar, margins and panel
        region -= QRegion(grabGeometry)
        self.setMask(region)

        # update the grab size according to grabWidget geometry
        # self.widthLabel.setText(str(self.grabWidget.width()))
        # self.heightLabel.setText(str(self.grabWidget.height()))
        

    def resizeEvent(self, event):
        super(Grabber, self).resizeEvent(event)
        # the first resizeEvent is called *before* any first-time showEvent and
        # paintEvent, there's no need to update the mask until then; see below
        if not self.dirty:
            # print("rezise event")
            self.updateMask()


    def moveEvent(self, event):
        super(Grabber, self).moveEvent(event)
        if not self.dirty:
            # print("Moving it")
            self.updateMask()

    def paintEvent(self, event):
        super(Grabber, self).paintEvent(event)
        # on Linux the frameGeometry is actually updated "sometime" after show()
        # is called; on Windows and MacOS it *should* happen as soon as the first
        # non-spontaneous showEvent is called (programmatically called: showEvent
        # is also called whenever a window is restored after it has been
        # minimized); we can assume that all that has already happened as soon as
        # the first paintEvent is called; before then the window is flagged as
        # "dirty", meaning that there's no need to update its mask yet.
        # Once paintEvent has been called the first time, the geometries should
        # have been already updated, we can mark the geometries "clean" and then
        # actually apply the mask.
        if self.dirty:
            self.updateMask()
            self.dirty = False

    def close_window(self):
        self.close()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    queue = Queue()
    queue2 = Queue()
    import threading
    abx = threading.Lock()
    grabber = Grabber(1000, 600, 300, 400, queue, queue2, abx)
    # grabber.show()
    sys.exit(app.exec_())

