import sys
import threading as threading
from multiprocessing import Process, Queue

import numpy as numpy
from os.path import basename
from PyQt5.QtCore import QPoint, Qt, QRect, QTimer
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication, QPushButton, QMenu, QFileDialog
from PyQt5.QtChart import QChart, QChartView, QHorizontalBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen


import faceReader_draw_image
import faceReader_box
from faceReader_model import FaceReader

def model_worker(inputs_queue, outputs_queue,x,y,w,h):
    while True:
        if not inputs_queue.empty():
            print(f'Receiving message')
            message = inputs_queue.get()
            print(f'message:', message)
            if message == 'STOP':
                print(f'stopping')
                break
            elif message == "start":
                model = FaceReader(x,y,w,h, outputs_queue)
                count = 0
                while True:
                    if not inputs_queue.empty():
                        message = inputs_queue.get()
                        print(f'message:', message)
                        if message == 'STOP':
                            print(f'stopping')
                            break
                    else:
                        model.run(count)
                        count += 1 
                        if count > 200:
                            count = 0
# def model_worker2(inputs_queue, outputs_queue,x,y,w,h):
#     while True:
#         if not inputs_queue.empty():
#             print(f'Receiving message')
#             message = inputs_queue.get()
#             print(f'message:', message)
#             if message == 'STOP2':
#                 print(f'stopping')
#                 break
#             elif message == "start2":
#                 model = FaceReader(x,y,w,h, outputs_queue)
#                 count = 0
#                 while True:
#                     if not inputs_queue.empty():
#                         message = inputs_queue.get()
#                         print(f'message:', message)
#                         if message == 'STOP2':
#                             print(f'stopping')
#                             break
#                     else:
#                         model.run(count)
#                         count += 1 
#                         if count > 200:
#                             count = 0

# def model_worker3(inputs_queue, outputs_queue,x,y,w,h):
#     while True:
#         if not inputs_queue.empty():
#             print(f'Receiving message')
#             message = inputs_queue.get()
#             print(f'message:', message)
#             if message == 'STOP3':
#                 print(f'stopping')
#                 break
#             elif message == "start3":
#                 model = FaceReader(x,y,w,h, outputs_queue)
#                 count = 0
#                 while True:
#                     if not inputs_queue.empty():
#                         message = inputs_queue.get()
#                         print(f'message:', message)
#                         if message == 'STOP3':
#                             print(f'stopping')
#                             break
#                     else:
#                         model.run(count)
#                         count += 1 
#                         if count > 200:
#                             count = 0

# def model_worker4(inputs_queue, outputs_queue,x,y,w,h):
#     while True:
#         if not inputs_queue.empty():
#             print(f'Receiving message')
#             message = inputs_queue.get()
#             print(f'message:', message)
#             if message == 'STOP4':
#                 print(f'stopping')
#                 break
#             elif message == "start4":
#                 model = FaceReader(x,y,w,h, outputs_queue)
#                 count = 0
#                 while True:
#                     if not inputs_queue.empty():
#                         message = inputs_queue.get()
#                         print(f'message:', message)
#                         if message == 'STOP4':
#                             print(f'stopping')
#                             break
#                     else:
#                         model.run(count)
#                         count += 1 
#                         if count > 200:
#                             count = 0

class Menu(QMainWindow):
    default_title = "FaceNet"
    face_box = None
    face_reader = None


    # numpy_image is the desired image we want to display given as a numpy array.
    def __init__(self, numpy_image=None, opacity=1, start_position=(300, 300, 550, 500)):
        super().__init__()   
        self.opacity = opacity
        self.drawing = False
        self.brushSize = 1
        self.brushColor = Qt.red
        self.lastPoint = QPoint()
        self.total_snips = 0
        self.title = Menu.default_title
        self.model_running = False
        self.box_x = None
        self.box_y = None
        self.box_w = None
        self.box_h = None
        self.box_drawn_can_start = False

        self.face_anger_digust = 0
        self.face_happy = 0
        self.face_neutral = 0
        self.face_sadness = 0
        self.face_surprise_fear = 0

        self.face_lock = threading.Lock()
        self.face_confidence_level = numpy.zeros((1,5))
        self.face_confidence_entry_count = 0
        
        self.emotion_set = None
        self.create_graph()

        self._timer = QTimer()
        self._timer.setInterval(33)
        self._timer.timeout.connect(self.calculate_emotion)
        self._timer.start()

        self._graph_timer = None
        

        self.face_model_process = None
        # self.face_model_process2 = None
        # self.face_model_process3 = None
        # self.face_model_process4 = None
        self.inputs_queue = Queue()
        self.outputs_queue = Queue()
        
        # New snip
        new_snip_action = QAction("Draw Box", self)
        new_snip_action.triggered.connect(self.__new_image_window)

        close_box = QAction('Close Box', self)
        close_box.triggered.connect(self.__close_box)

        run_program = QAction('start program', self)
        run_program.triggered.connect(self.__start_program)

        stop_program = QAction('stop program', self)
        stop_program.triggered.connect(self.__stop_program)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(new_snip_action)
        self.toolbar.addAction(close_box)
        self.toolbar.addAction(run_program)
        self.toolbar.addAction(stop_program)

        self.snippingTool = faceReader_draw_image.SnippingWidget(self)
        self.setGeometry(*start_position)

        # From the second initialization, both arguments will be valid
        
        self.image = QPixmap("background.PNG")

        self.show()

    def create_graph(self):
        self.emotion_set = QBarSet('Confidence Level')

        self.emotion_set.append([self.face_anger_digust, self.face_happy, self.face_neutral, self.face_sadness, self.face_surprise_fear])

        series = QHorizontalBarSeries()
        series.append(self.emotion_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('ReLuu FaceReader')

        chart.setAnimationOptions(QChart.SeriesAnimations)

        months = ('Angery and Disgusted', 'Happy', 'Neutral', 'Sadness', 'Fear and Surprise')

        axisY = QBarCategoryAxis()
        axisY.append(months)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        axisX = QValueAxis()
        axisX.setMax(1.0)
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisX.applyNiceNumbers()

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chartView)


    def __new_image_window(self):
        self.snippingTool.start()
    
    def __create_box(self, x,y,w,h):
        Menu.face_box = faceReader_box.Box(x,y,w,h)
        self.box_x = x
        self.box_y = y
        self.box_w = w
        self.box_h = h
        self.box_drawn_can_start = True

    def __start_program(self):
        if self.box_drawn_can_start and not self.model_running:
            self._graph_timer = QTimer()
            self._graph_timer.setInterval(1000)
            self._graph_timer.timeout.connect(self.__graph)
            self._graph_timer.start()

            self.face_model_process = Process(target=model_worker, args=(self.inputs_queue, self.outputs_queue, 
                                            self.box_x, self.box_y, self.box_w, self.box_h))
            self.face_model_process.start()
            self.model_running = True
            self.inputs_queue.put("start")
            # self.face_model_process2 = Process(target=model_worker2, args=(self.inputs_queue, self.outputs_queue, 
            #                                 self.box_x, self.box_y, self.box_w, self.box_h))
            # self.face_model_process2.start()
            # self.inputs_queue.put("start2")

            # self.face_model_process3 = Process(target=model_worker3, args=(self.inputs_queue, self.outputs_queue, 
            #                                 self.box_x, self.box_y, self.box_w, self.box_h))
            # self.face_model_process3.start()
            # self.inputs_queue.put("start3")

            # self.face_model_process4 = Process(target=model_worker4, args=(self.inputs_queue, self.outputs_queue, 
            #                                 self.box_x, self.box_y, self.box_w, self.box_h))
            # self.face_model_process4.start()
            # self.inputs_queue.put("start4")
        elif not self.box_drawn_can_start:
            print("---Cannot start program, box not drawn---")
        else:
            print("---model running___")
        
    def calculate_emotion(self):
        if not self.outputs_queue.empty():
            self.face_lock.acquire()

            self.face_confidence_entry_count +=1
            face_confidence_output = self.outputs_queue.get()
            self.face_confidence_level += face_confidence_output
            self.face_lock.release()

    def __stop_program(self):
        if self.face_model_process is not None:    
            self.face_model_process.terminate()
            # self.face_model_process2.terminate()
            # self.face_model_process3.terminate()
            # self.face_model_process4.terminate()
            print("---closing model---")
            self.model_running = False
            self._graph_timer.stop()

    def __close_box(self):
        if Menu.face_box:
            self.__stop_program()
            Menu.face_box.close_window()
            self.box_drawn_can_start = False
            print("---closing box---")

    def __graph(self):
        self.face_lock.acquire()

        new_graph_value = self.face_confidence_level / self.face_confidence_entry_count
        print(str(new_graph_value))

        self.face_anger_digust = new_graph_value[0][0]
        self.face_happy = new_graph_value[0][1]
        self.face_neutral = new_graph_value[0][2]
        self.face_sadness = new_graph_value[0][3]
        self.face_surprise_fear = new_graph_value[0][4]

        self.emotion_set.append([self.face_anger_digust, self.face_happy, self.face_neutral, self.face_sadness, self.face_surprise_fear])

        self.face_confidence_level = numpy.zeros((1,5))
        self.face_confidence_entry_count = 0
        self.face_lock.release()
        

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

