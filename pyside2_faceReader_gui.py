import sys
import threading as threading
from multiprocessing import Process, Queue

import numpy as numpy
import PySide2.QtCharts
from os.path import basename
from PySide2.QtCore import QPoint, Qt, QRect, QTimer
from PySide2.QtWidgets import QAction, QMainWindow, QApplication, QPushButton, QMenu, QFileDialog
from PySide2.QtGui import QPixmap, QImage, QPainter, QPen
from PySide2.QtCharts import QtCharts

import pyside2_faceReader_draw_image
from pyside2_faceReader_box_movable import Grabber
from pyside2_faceReader_model import FaceReader

from random import random

import datetime

global_model_start = False

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
                start1 = datetime.datetime.now()
                print("################## starting")
                model = FaceReader(outputs_queue)
                count = 0
                x1 = x
                y1 = y
                width = w
                height = h
                print("################## ending")
                start2 = datetime.datetime.now()
                print(start2-start1)
                while True:
                    #Use multiple queues
                    if not inputs_queue.empty():
                        message = inputs_queue.get()
                        print(f'message:', message)
                        if "UPDATE" in message:
                            new_cords = message.split(" ")
                            x1 = int(new_cords[1])
                            y1 = int(new_cords[2])
                            width = x1+int(new_cords[3])
                            height = y1+int(new_cords[4])
                        elif message == 'STOP':
                            print(f'stopping')
                            break
                        else:
                            continue
                    else:
                        model.run(x1, y1, width, height, count)
                        count += 1 
                        if count > 200:
                            count = 0

class Menu(QMainWindow):
    default_title = "ReLuu FaceReader"
    face_box = None
    face_reader = None

    def __init__(self, numpy_image=None, start_position=(200, 300, 550, 500)):
        super().__init__()   
        self.drawing = False
        self.brushSize = 1
        self.brushColor = Qt.red
        self.lastPoint = QPoint()
        self.total_snips = 0
        self.setWindowTitle(Menu.default_title)
        self.box_x = None
        self.box_y = None
        self.box_w = None
        self.box_h = None

        self.model_running = False
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

        self.inputs_queue = Queue()
        self.outputs_queue = Queue()
        #Seems clunky, idk
        self.update_position_queue = Queue(1)
        self.update_position_lock = threading.Lock()

        self._graph_timer = QTimer()
        self._graph_timer.setInterval(2000)
        self._graph_timer.timeout.connect(self.create_graph)

        # self.delete_timer = QTimer()
        # self.delete_timer.setInterval(1500)        
        # self.delete_timer.timeout.connect(self.print_cords_forme)
        # self.delete_timer.start()

        # self.delete_timer2 = QTimer()
        # self.delete_timer2.setInterval(33)        
        # self.delete_timer2.timeout.connect(self.update_position_model_not_running)
        # self.delete_timer2.start()

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

        self.snippingTool = pyside2_faceReader_draw_image.SnippingWidget(self)
        self.setGeometry(*start_position)

        self.show()


    def create_graph(self):
        self.face_lock.acquire()
        self.emotion_set = QtCharts.QBarSet('Confidence Level')

        new_graph_value = self.face_confidence_level / self.face_confidence_entry_count
        print(f"----- New graph value{str(new_graph_value)}--------------")

        self.face_anger_digust = new_graph_value[0][0]
        self.face_happy = new_graph_value[0][1]
        self.face_neutral = new_graph_value[0][2]
        self.face_sadness = new_graph_value[0][3]
        self.face_surprise_fear = new_graph_value[0][4]

        self.emotion_set.append([self.face_anger_digust, self.face_happy, self.face_neutral, self.face_sadness, self.face_surprise_fear])
        series = QtCharts.QHorizontalBarSeries()

        series.append(self.emotion_set)

        self.face_confidence_level = numpy.zeros((1,5))
        self.face_confidence_entry_count = 0
        self.face_lock.release()
        chart = QtCharts.QChart()
        chart.addSeries(series)
        chart.setTitle('ReLuu FaceReader')
        # chart.setAnimationOptions(QtCharts.SeriesAnimations)
        emotions = ('Angery and Disgusted', 'Happy', 'Neutral', 'Sadness', 'Fear and Surprise')

        axisY = QtCharts.QBarCategoryAxis()
        axisY.append(emotions)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        axisX = QtCharts.QValueAxis()
        axisX.setMax(1.0)
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisX.applyNiceNumbers()

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartView = QtCharts.QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(chartView)
   

    def __new_image_window(self):
        self.snippingTool.start()


    def __create_box(self, x,y,w,h):
        width = w-x
        height = h-y
        Menu.face_box = Grabber(x,y,width,height, self.inputs_queue, self.update_position_queue, self.update_position_lock)
        self.box_x = x
        self.box_y = y
        self.box_w = w
        self.box_h = h
        self.box_drawn_can_start = True


    def __start_program(self):
        if self.box_drawn_can_start and not self.model_running:
            self.update_position_lock.acquire()
            self._graph_timer.start()

            if not self.update_position_queue.empty():
                message = self.update_position_queue.get()
                new_cords = message.split(" ")
                self.box_x = int(new_cords[1])
                self.box_y = int(new_cords[2])
                self.box_w = self.box_x+int(new_cords[3])
                self.box_h = self.box_y+int(new_cords[4])

            self.update_position_queue.put(message) 
            self.face_model_process = Process(target=model_worker, args=(self.inputs_queue, self.outputs_queue, self.box_x, self.box_y, self.box_w, self.box_h))
            
            self.face_model_process.start()
            self.model_running = True
            self.inputs_queue.put("start")
            self.update_position_lock.release()
        elif not self.box_drawn_can_start:
            print("---Cannot start program, box not drawn---")
        else:
            print("---model running___")


    # Only used when the model is not running
    # def update_position_model_not_running(self):
    #     if not global_model_start:
    #         if not self.inputs_queue.empty():
    #             message = self.inputs_queue.get()
    #             print(f'message:', message)
    #             if "UPDATE" in message:
    #                 new_cords = message.split(" ")
    #                 self.box_x = int(new_cords[1])
    #                 self.box_y = int(new_cords[2])
    #                 self.box_w = self.box_x+int(new_cords[3])
    #                 self.box_h = self.box_y+int(new_cords[4])
    

    # def print_cords_forme(self):
    #     if not global_model_start:
    #         print("printing cords")
    #         print(self.box_x, self.box_y, self.box_w, self.box_h)  


    def calculate_emotion(self):
        if not self.outputs_queue.empty():
            self.face_lock.acquire()
            self.face_confidence_entry_count +=1
            face_confidence_output = self.outputs_queue.get()
            self.face_confidence_level += face_confidence_output
            print("-------emotion calculated-------")
            self.face_lock.release()


    def __stop_program(self):
        if self.face_model_process is not None:    
            self.face_model_process.terminate()
            self._graph_timer.stop()
            self.model_running = False
            print("---closing model---")


    def __close_box(self):
        if Menu.face_box:
            self.__stop_program()
            Menu.face_box.close_window()
            self.box_drawn_can_start = False
            print("---closing box---")


    def __graph(self):
        self.face_lock.acquire()
        print("updating graph...")
        r1 = random()
        r2 = random()
        r3 = random()
        r4 = random()
        r5 = random()

        self.face_anger_digust = r1
        self.face_happy = r2
        self.face_neutral = r3
        self.face_sadness = r4
        self.face_surprise_fear = r5

        self.emotion_set.append([self.face_anger_digust, self.face_happy, self.face_neutral, self.face_sadness, self.face_surprise_fear])

        # self.face_confidence_level = numpy.zeros((1,5))
        # self.face_confidence_entry_count = 0

        # new_graph_value = self.face_confidence_level / self.face_confidence_entry_count
        # print(str(new_graph_value))

        # self.face_anger_digust = new_graph_value[0][0]
        # self.face_happy = new_graph_value[0][1]
        # self.face_neutral = new_graph_value[0][2]
        # self.face_sadness = new_graph_value[0][3]
        # self.face_surprise_fear = new_graph_value[0][4]

        # self.emotion_set.append([self.face_anger_digust, self.face_happy, self.face_neutral, self.face_sadness, self.face_surprise_fear])

        # self.face_confidence_level = numpy.zeros((1,5))
        # self.face_confidence_entry_count = 0
        self.face_lock.release()

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

    def closeEvent(self, event):
        Menu.face_box.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = Menu()
    sys.exit(app.exec_())

