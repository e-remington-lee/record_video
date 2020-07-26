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
    def __init__(self, x, y, w, h, inputs_queue):
        QWidget.__init__(self)   
        # center title!     
        self.setWindowTitle('ReLuu FaceReader')
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.inputs_queue = inputs_queue
        self.setGeometry(self.x, self.y, self.w, self.h)
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

        ######
        self.panel = QWidget()
        layout.addWidget(self.panel)
        panelLayout = QHBoxLayout()
        self.panel.setLayout(panelLayout)
        panelLayout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(1, 1, 1, 1)

        self.configButton = QPushButton(self.style().standardIcon(QStyle.SP_ComputerIcon), '')
        self.configButton.setFlat(True)
        panelLayout.addWidget(self.configButton)

        panelLayout.addWidget(VLine())

        self.fpsSpinBox = QSpinBox()
        panelLayout.addWidget(self.fpsSpinBox)
        self.fpsSpinBox.setRange(1, 50)
        self.fpsSpinBox.setValue(15)
        panelLayout.addWidget(QLabel('fps'))

        panelLayout.addWidget(VLine())

        self.widthLabel = QLabel()
        panelLayout.addWidget(self.widthLabel)
        self.widthLabel.setFrameShape(QLabel.StyledPanel)

        panelLayout.addWidget(QLabel('x'))

        self.heightLabel = QLabel()
        panelLayout.addWidget(self.heightLabel)
        self.heightLabel.setFrameShape(QLabel.StyledPanel)
        ######

        self.show()

    def updateMask(self):
        # get the *whole* window geometry, including its titlebar and borders
        frameRect = self.frameGeometry()

        # get the grabWidget geometry and remap it to global coordinates
        grabGeometry = self.grabWidget.geometry()
        grabGeometry.moveTopLeft(self.grabWidget.mapToGlobal(QPoint(0, 0)))

        # get the actual margins between the grabWidget and the window margins
        left = frameRect.left() - grabGeometry.left()
        top = frameRect.top() - grabGeometry.top()
        right = frameRect.right() - grabGeometry.right()
        bottom = frameRect.bottom() - grabGeometry.bottom()
        print(self.grabWidget.pos())

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
        self.widthLabel.setText(str(self.grabWidget.width()))
        self.heightLabel.setText(str(self.grabWidget.height()))
        

    def resizeEvent(self, event):
        super(Grabber, self).resizeEvent(event)
        # the first resizeEvent is called *before* any first-time showEvent and
        # paintEvent, there's no need to update the mask until then; see below
        if not self.dirty:
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
    grabber = Grabber(1000, 600, 300, 400, 10)
    # grabber.show()
    sys.exit(app.exec_())