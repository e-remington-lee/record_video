import sys

import matplotlib
import numpy as np
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from active_model import Ui_active_model

# how to reuse embedded matplots
# https://stackoverflow.com/questions/53258160/update-an-embedded-matplotlib-plot-in-a-pyqt5-gui-with-toolbar

# plot a color map
# https://stackoverflow.com/questions/16834861/create-own-colormap-using-matplotlib-and-plot-color-scale

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=1, height=1, dpi=20):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
        self.setParent(parent)
        self.norm=plt.Normalize(-1,1)
        self.cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red","white","green"])
        


    def plot(self):
        # ax = self.fig.add_subplot(111)
        self.axes.cla()
        x,y,c = zip(*np.random.rand(1,3)*2-1)
        self.axes.axis("off")        
        self.axes.scatter(x,y,c=c, s=5000, cmap=self.cmap, norm=self.norm)
        self.fig.canvas.draw_idle()
        # plt.colorbar()
        # plt.show()


class MainWindow(QtWidgets.QWidget, Ui_active_model):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        icon = QtGui.QIcon("reluu_application/GUI_improvements/logo_transparent_background.png")
        self.setWindowIcon(icon)
        self.abc = False
        # import os
        # print(os.listdir())

        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.sc.plot()
        self.emotion_icon_layout.addWidget(self.sc) 
        # self.emotion_icon_layout.setHidden(True)

        # button1 = QtWidgets.QPushButton("push", clicked=self.idk)
        # self.layout.addWidget(button1)
        # self.setLayout(self.layout)
        self.show()
        self.stop_session_button.clicked.connect(self.idk)
        self.detailed_view_checkbox.stateChanged.connect(self.show_details)
    
    def show_details(self):
        if self.detailed_view_checkbox.isChecked():
            self.resize(248, 450)
        else:
            self.resize(248, 304)


    def idk(self):
        self.show_details()
        self.sc.plot()
        self.abc = not self.abc
        self.warning_label1.setHidden(self.abc)
        self.warning_label2.setHidden(self.abc)


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
# import sys

# from PySide2.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
# from PySide2.QtGui import QIcon

# import matplotlib
# import numpy as np
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
# import matplotlib.pyplot as plt

# import random

# class App(QMainWindow):

#     def __init__(self):
#         super().__init__()
#         self.left = 100
#         self.top = 100
#         self.title = 'PyQt5 matplotlib example - pythonspot.com'
#         self.width = 640
#         self.height = 400
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)

#         m = PlotCanvas(self, width=5, height=4)
#         m.move(0,0)

#         button = QPushButton('PyQt5 button', self)
#         button.setToolTip('This s an example button')
#         button.move(500,0)
#         button.resize(140,100)

#         self.show()


# class PlotCanvas(FigureCanvas):

#     def __init__(self, parent=None, width=5, height=4, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = fig.add_subplot(111)

#         FigureCanvas.__init__(self, fig)
#         self.setParent(parent)

#         FigureCanvas.setSizePolicy(self,
#                 QSizePolicy.Expanding,
#                 QSizePolicy.Expanding)
#         FigureCanvas.updateGeometry(self)
#         self.plot()


#     def plot(self):
#         data = [random.random() for i in range(25)]
#         ax = self.figure.add_subplot(111)
#         ax.axis("off")
#         ax.plot(data, 'r-')
#         self.draw()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = App()
#     sys.exit(app.exec_())