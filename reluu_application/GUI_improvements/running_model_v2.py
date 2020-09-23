import sys
from multiprocessing import Queue, Process
from threading import Lock

import matplotlib
import numpy as np
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from active_model2 import Ui_active_model
import login_menu
import image_box_movable
import reluu_model

# how to reuse embedded matplots
# https://stackoverflow.com/questions/53258160/update-an-embedded-matplotlib-plot-in-a-pyqt5-gui-with-toolbar

# plot a color map
# https://stackoverflow.com/questions/16834861/create-own-colormap-using-matplotlib-and-plot-color-scale

def model_worker(inputs_queue, outputs_queue, x,y,w,h):
    while True:
        if not inputs_queue.empty():
            print(f'Receiving message')
            message = inputs_queue.get()
            print(f'message:', message)
            if message == 'STOP':
                print(f'stopping')
                break
            elif message == "start":
                model = reluu_model.ReluuModel(outputs_queue)
                x1 = x
                y1 = y
                width = w
                height = h
                while True:
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
                        # take image here, then input that into the functions
                        model.run(x1, y1, width, height)



class ActiveModelWindow(QtWidgets.QWidget, Ui_active_model):
    def __init__(self, face_box_x, face_box_y, face_box_w, face_box_h, *args, **kwargs):
        super(ActiveModelWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle('ReLuu')
        icon = QtGui.QIcon("reluu_application/GUI_improvements/logo_transparent_background.png")
        self.setWindowIcon(icon)
        self.face_box_x = face_box_x
        self.face_box_y = face_box_y
        self.face_box_w = face_box_w
        self.face_box_h = face_box_h
        self.width = self.face_box_w - self.face_box_x
        self.height = self.face_box_h - self.face_box_y
        self.inputs_queue, self.outputs_queue = Queue(), Queue()
        self.update_position_lock = Lock()
        ActiveModelWindow.image_box = image_box_movable.ImageBox(face_box_x, face_box_y, self.width, self.height, 
                                            self.inputs_queue, self.update_position_lock)
        self.emotion_lock = Lock()
        self.face_anger_digust = 0
        self.face_happy = 0
        self.face_neutral = 0
        self.face_sadness = 0
        self.face_surprise_fear = 0
        self.face_confidence_level = np.zeros((1,5))
        self.face_confidence_entry_count = 0

        self.model_timer = QtCore.QTimer()
        self.model_timer.setInterval(33)
        self.model_timer.timeout.connect(self.calculate_emotion)

        self.no_face_warning_timer = QtCore.QTimer()
        self.no_face_warning_timer.setInterval(1000)
        self.no_face_warning_timer.timeout.connect(self.show_no_face_warning)
        self.no_face_count = 0      

        self.graph_timer = QtCore.QTimer()
        self.graph_timer.setInterval(3000)
        self.graph_timer.timeout.connect(self.update_graphs)

        self.reluu_model_process = None

        self.resize(300, 520)
        self.detailed_view = DetailedView(self, width=1, height=2, dpi=100)
        self.detailed_view.plot(self.face_confidence_level)
        self.detailed_view_layout.addWidget(self.detailed_view)
        # self.detailed_view.axes.set_visible(False)
        self.error = False
        self.emotion_icon = EmotionIcon(self, width=1, height=1, dpi=100)
        self.emotion_icon.plot(0)
        self.emotion_icon_layout.addWidget(self.emotion_icon)

        self.stop_session_button.clicked.connect(self.stop_model)
        self.detailed_view_checkbox.stateChanged.connect(self.show_details)
        self.warning_label1.setHidden(True)
        self.warning_label2.setHidden(True)
        self.show()
        self.start_reluu_model()
    
    def show_details(self):
        if self.detailed_view_checkbox.isChecked():
            self.detailed_view.visible()
        else:
            # self.resize(300, 320)
            self.detailed_view.invisible()


    def start_reluu_model(self):
        self.model_timer.start()
        self.graph_timer.start()
        self.no_face_warning_timer.start()
        self.update_position_lock.acquire()
        self.reluu_model_process = Process(target=model_worker, 
                                            args=(self.inputs_queue, self.outputs_queue,
                                            self.face_box_x, self.face_box_y, self.face_box_w, self.face_box_h))
        self.reluu_model_process.start()
        self.inputs_queue.put("start")
        self.update_position_lock.release()


    def calculate_emotion(self):
        if not self.outputs_queue.empty():
            self.emotion_lock.acquire()            
            face_confidence_output = self.outputs_queue.get()
            self.face_confidence_entry_count +=1
            self.face_confidence_level = np.add(self.face_confidence_level, face_confidence_output)
            print("-------emotion calculated-------")
            self.no_face_count = 0
            self.show_warning = True
            self.emotion_lock.release()
        else:
            self.no_face_count +=1
            if self.no_face_count >= 20:
                self.show_warning = False

    def show_no_face_warning(self):
        self.warning_label1.setHidden(self.show_warning)
        self.warning_label2.setHidden(self.show_warning)

    def update_graphs(self):
        self.emotion_lock.acquire()
        new_graph_value = self.face_confidence_level / self.face_confidence_entry_count
        self.detailed_view.plot(new_graph_value)
        colormap_values = np.array([[-1, 1, 0, -0.2, -0.2]])
        step1 = np.multiply(new_graph_value,colormap_values)
        colormap_result = np.sum(step1)
        self.emotion_icon.plot(colormap_result)
        self.face_confidence_entry_count = 0
        self.face_confidence_level = np.zeros((1,5))
        self.emotion_lock.release()

    def stop_model(self):
        self.reluu_model_process.terminate()
        if self.reluu_model_process is not None:
            self.reluu_model_process.terminate()
        ActiveModelWindow.image_box.close()
        self.model_timer.stop()
        self.graph_timer.stop()
        self.no_face_warning_timer.stop()
        self.close()
        self.login_menu = login_menu.MainMenu()
        self.login_menu.show()

    def closeEvent(self, event):
        self.stop_model()
        event.accept()


class EmotionIcon(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=1, height=1, dpi=20):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(EmotionIcon, self).__init__(self.fig)
        self.setParent(parent)
        self.norm=plt.Normalize(-1,1)
        self.cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red","whitesmoke","green"])


    def plot(self, data):
        # ax = self.fig.add_subplot(111)
        # c = np.random.rand(1,1)*2-1
        self.axes.cla()
        self.axes.axis("off")        
        self.axes.scatter(1,1,c=data, s=5000, cmap=self.cmap, norm=self.norm)
        self.fig.canvas.draw_idle()
        # plt.colorbar()
        # plt.show()
    
    def invisible(self):
        pass


class DetailedView(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=1, height=1, dpi=20):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.subplots_adjust(left=0.3)
        self.axes = self.fig.add_subplot(111)        
        self.emotions = ["Anger", "Happy", "Neutral", "Saddness", "Surprise"]
        self.axes.set_visible(False)        
        # Once I figure out how to add data to axis...
        # self.axes.get_xaxis().set_visible(False)

        super(DetailedView, self).__init__(self.fig)
        self.setParent(parent)


    def plot(self, data):
        self.axes.cla()      
        data2 = data.tolist()
        self.axes.barh(self.emotions, data2[0], color="black")
        self.axes.set_title("Emotion")
        self.axes.set_xlim([0,1])
        self.fig.canvas.draw_idle()
        

    def visible(self):
        self.axes.set_visible(True)
        self.fig.canvas.draw_idle()


    def invisible(self):
        self.axes.set_visible(False)
        self.fig.canvas.draw_idle()
        # self.figure.close()
        # https://stackoverflow.com/questions/8213522/when-to-use-cla-clf-or-close-for-clearing-a-plot-in-matplotlib


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # q1, q2 = Queue(), Queue()
    w = ActiveModelWindow(700,700,1000,1000)
    app.exec_()