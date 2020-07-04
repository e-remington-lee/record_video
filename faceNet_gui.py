import sys
from os.path import basename
from PyQt5.QtCore import QPoint, Qt, QRect
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication, QPushButton, QMenu, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen

import faceNet_draw_image
import faceNet_box
import emotion_detect_5_in_gui

class Menu(QMainWindow):
    default_title = "FaceNet"
    # face_chosen = False
    face_box = None

    # numpy_image is the desired image we want to display given as a numpy array.
    def __init__(self, numpy_image=None, opacity=1, start_position=(300, 300, 350, 250)):
        super().__init__()

        self.opacity = opacity
        self.drawing = False
        self.brushSize = 1
        self.brushColor = Qt.red
        self.lastPoint = QPoint()
        self.total_snips = 0
        self.title = Menu.default_title

        self.box_x = None
        self.box_y = None
        self.box_w = None
        self.box_h = None
        self.box_drawn_can_start = False
        
        # New snip
        new_snip_action = QAction("Draw Box", self)
        new_snip_action.setShortcut('Ctrl+N')
        new_snip_action.setStatusTip('Snip!')
        new_snip_action.triggered.connect(self.new_image_window)

        close_box = QAction('Close Box', self)
        close_box.triggered.connect(self.close_box)

        run_program = QAction('start program', self)
        run_program.triggered.connect(self.start_program)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(new_snip_action)
        self.toolbar.addAction(close_box)
        self.toolbar.addAction(run_program)

        self.snippingTool = faceNet_draw_image.SnippingWidget(self)
        self.setGeometry(*start_position)

        # From the second initialization, both arguments will be valid
        
        self.image = QPixmap("background.PNG")

        self.show()

    def new_image_window(self):
        self.snippingTool.start()
    
    def create_box(self, x,y,w,h):
        # if not Menu.face_chosen:
        Menu.face_box = faceNet_box.Box(x,y,w,h)
        self.box_x = x
        self.box_y = y
        self.box_w = w
        self.box_h = h
        self.box_drawn_can_start = True
        # else: 
        #     Menu.face_box.close()
        #     Menu.face_box = box.Box(x,y,w,h)

    def start_program(self):
        if self.box_drawn_can_start:
            emotion_detect_5_in_gui.main(self.box_x,self.box_y,self.box_w,self.box_h)

    def close_box(self):
        if Menu.face_box:
            Menu.face_box.close_window()
            self.box_drawn_can_start = False

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = QRect(0,  self.toolbar.height(), self.image.width(), self.image.height())
        painter.drawPixmap(rect, self.image)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos() - QPoint(0, self.toolbar.height())

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos() - QPoint(0, self.toolbar.height()))
            self.lastPoint = event.pos() - QPoint(0, self.toolbar.height())
            self.update()

    def mouseReleaseEvent2(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False
        

    # TODO exit application when we exit all windows
    def closeEvent(self, event):
        event.accept()

    @staticmethod
    def convert_numpy_img_to_qpixmap(np_img):
        height, width, channel = np_img.shape
        bytesPerLine = 3 * width
        return QPixmap(QImage(np_img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = Menu()
    sys.exit(app.exec_())
