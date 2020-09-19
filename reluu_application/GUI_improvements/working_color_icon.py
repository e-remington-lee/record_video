import sys
import matplotlib
import numpy as np

from PySide2 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


# plot a color map
# https://stackoverflow.com/questions/16834861/create-own-colormap-using-matplotlib-and-plot-color-scale

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
        self.setParent(parent)

    def plot(self):
        # ax = self.fig.add_subplot(111)
        self.axes.cla()
        x,y,c = zip(*np.random.rand(1,3)*2-1)
        norm=plt.Normalize(-1,1)
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red","white","green"])
        
        self.axes.axis("off")
        self.axes.scatter(x,y,c=c, s=5000, cmap=cmap, norm=norm)
        self.fig.canvas.draw_idle()
        # plt.colorbar()
        # plt.show()


class MainWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # Create the maptlotlib FigureCanvas object, 
        # which defines a single set of axes as self.axes.
        self.layout = QtWidgets.QVBoxLayout()

        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.sc.plot()
        self.layout.addWidget(self.sc)       

        button1 = QtWidgets.QPushButton("push", clicked=self.idk)
        self.layout.addWidget(button1)
        self.setLayout(self.layout)
        # self.setCentralWidget(sc)
        self.show()

    def idk(self):
        self.sc.plot()


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