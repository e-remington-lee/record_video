import sys

import matplotlib
import numpy as np
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from active_model2 import Ui_active_model

# how to reuse embedded matplots
# https://stackoverflow.com/questions/53258160/update-an-embedded-matplotlib-plot-in-a-pyqt5-gui-with-toolbar

# plot a color map
# https://stackoverflow.com/questions/16834861/create-own-colormap-using-matplotlib-and-plot-color-scale

class EmotionIcon(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=1, height=1, dpi=20):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(EmotionIcon, self).__init__(self.fig)
        self.setParent(parent)
        self.norm=plt.Normalize(-1,1)
        self.cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red","aliceblue","green"])


    def plot(self):
        # ax = self.fig.add_subplot(111)
        c = np.random.rand(1,1)*2-1
        self.axes.cla()
        self.axes.axis("off")        
        self.axes.scatter(1,1,c=c, s=5000, cmap=self.cmap, norm=self.norm)
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


    def plot(self):
        self.axes.cla()      
        index = [0,1,2,3,4]
        data = [0.10, 0.7, 0.0, 0.0, .20]
        self.axes.barh(self.emotions, data, color="darkturquoise")
        self.axes.set_title("Emotion")
        self.axes.set_xlim([0,1])
        # for i, v in enumerate(data):
        #     self.axes.text(i, str(v))
        self.fig.canvas.draw_idle()
        

    def visible(self):
        self.axes.set_visible(True)
        self.fig.canvas.draw_idle()


    def invisible(self):
        self.axes.set_visible(False)
        self.fig.canvas.draw_idle()
        # self.figure.close()
        # https://stackoverflow.com/questions/8213522/when-to-use-cla-clf-or-close-for-clearing-a-plot-in-matplotlib


class MainWindow(QtWidgets.QWidget, Ui_active_model):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        icon = QtGui.QIcon("reluu_application/GUI_improvements/logo_transparent_background.png")
        self.setWindowIcon(icon)

        self.resize(300, 520)
        self.detailed_view = DetailedView(self, width=1, height=2, dpi=100)
        self.detailed_view.plot()
        self.detailed_view_layout.addWidget(self.detailed_view)
        # self.detailed_view.axes.set_visible(False)

        self.error = False

        self.ei = EmotionIcon(self, width=1, height=1, dpi=100)
        self.ei.plot()
        self.emotion_icon_layout.addWidget(self.ei)        

        self.stop_session_button.clicked.connect(self.idk)
        self.detailed_view_checkbox.stateChanged.connect(self.show_details)
        self.show()
    
    def show_details(self):
        if self.detailed_view_checkbox.isChecked():
            self.detailed_view.visible()
        else:
            # self.resize(300, 320)
            self.detailed_view.invisible()


    def idk(self):
        self.ei.plot()
        self.error = not self.error
        self.warning_label1.setHidden(self.error)
        self.warning_label2.setHidden(self.error)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec_()
