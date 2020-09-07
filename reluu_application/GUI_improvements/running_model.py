import sys
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
import login_menu


class RunningModel(QtWidgets.QWidget):
    def __init__(self,):
        super(RunningModel, self).__init__()

        self.win = QtWidgets.QPushButton("I did it", clicked=self.win2)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.win)
        self.setLayout(self.layout)

    def win2(self):
        print("I win for the night")



if __name__ == "__main__":
    app = QtWidgets.QApplication()
    w = RunningModel()
    w.show()
    sys.exit(app.exec_())