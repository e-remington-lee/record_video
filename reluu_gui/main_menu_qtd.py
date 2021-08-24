import os
import sys
import importlib.util

print('Importing local shiboken2')
abspath = os.path.dirname(os.path.abspath(sys.argv[0]))
MODULE_PATH2 = "./shiboken2/__init__.py"
MODULE_PATH2_ABS = os.path.join(abspath, "./shiboken2/__init__.py")
MODULE_NAME2 = "shiboken2"

spec2 = importlib.util.spec_from_file_location(MODULE_NAME2, MODULE_PATH2_ABS)
shiboken2 = importlib.util.module_from_spec(spec2)
sys.modules[spec2.name] = shiboken2
spec2.loader.exec_module(shiboken2)
print(shiboken2.__version__)

print('Importing local PySide2')
MODULE_PATH = "./PySide2/__init__.py"
MODULE_PATH_ABS = os.path.join(abspath, "./PySide2/__init__.py")
MODULE_NAME = "PySide2"

spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH_ABS)
PySide2 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = PySide2
spec.loader.exec_module(PySide2)
print(PySide2.__version__)

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_mainMenu(object):
    def setupUi(self, mainMenu):
        if not mainMenu.objectName():
            mainMenu.setObjectName(u"mainMenu")
        mainMenu.resize(400, 316)
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        mainMenu.setPalette(palette)
        mainMenu.setStyleSheet(u"QLineEdit {\n"
" border-radius: 5px;\n"
"border: 0.5px solid gray;\n"
"}\n"
"\n"
"QPushButton{\n"
"border-radius:5px;\n"
"background-color: #d5f6ff;\n"
"border: 0.5px solid gray;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"background-color: #befeff\n"
"}")
        self.horizontalLayout = QHBoxLayout(mainMenu)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.vbox_mainMenu = QVBoxLayout()
        self.vbox_mainMenu.setObjectName(u"vbox_mainMenu")
        self.logo_layout_mainMenu = QHBoxLayout()
        self.logo_layout_mainMenu.setObjectName(u"logo_layout_mainMenu")
        self.logo_mainMenu = QLabel(mainMenu)
        self.logo_mainMenu.setObjectName(u"logo_mainMenu")
        self.logo_mainMenu.setMaximumSize(QSize(150, 150))
        cur_dir = os.getcwd()
        # os.chdir(sys._MEIPASS)
        self.logo_mainMenu.setPixmap(QPixmap(u"reluu_gui\\auxiliary_files\\logo_transparent_background.png"))
        os.chdir(cur_dir)
        self.logo_mainMenu.setScaledContents(True)

        self.logo_layout_mainMenu.addWidget(self.logo_mainMenu, 0, Qt.AlignHCenter)


        self.vbox_mainMenu.addLayout(self.logo_layout_mainMenu)

        self.button_layout = QVBoxLayout()
        self.button_layout.setObjectName(u"button_layout")
        self.button_layout.setContentsMargins(30, -1, 30, -1)
        self.start_model_button = QPushButton(mainMenu)
        self.start_model_button.setObjectName(u"start_model_button")
        self.start_model_button.setMinimumSize(QSize(200, 0))
        font = QFont()
        font.setFamily(u"Segoe UI Symbol")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.start_model_button.setFont(font)
        self.start_model_button.setToolTipDuration(-1)

        self.button_layout.addWidget(self.start_model_button)

        self.feedback_button = QPushButton(mainMenu)
        self.feedback_button.setObjectName(u"feedback_button")
        self.feedback_button.setMinimumSize(QSize(200, 0))
        font1 = QFont()
        font1.setFamily(u"Segoe UI Symbol")
        font1.setPointSize(14)
        self.feedback_button.setFont(font1)

        self.button_layout.addWidget(self.feedback_button)

        self.sign_out_button = QPushButton(mainMenu)
        self.sign_out_button.setObjectName(u"sign_out_button")
        self.sign_out_button.setFont(font1)

        self.button_layout.addWidget(self.sign_out_button)


        self.vbox_mainMenu.addLayout(self.button_layout)

        self.spacing_layout_mainMenu = QHBoxLayout()
        self.spacing_layout_mainMenu.setObjectName(u"spacing_layout_mainMenu")
        self.spacing_layout_mainMenu.setContentsMargins(-1, 10, -1, -1)

        self.vbox_mainMenu.addLayout(self.spacing_layout_mainMenu)


        self.horizontalLayout.addLayout(self.vbox_mainMenu)


        self.retranslateUi(mainMenu)

        QMetaObject.connectSlotsByName(mainMenu)
    # setupUi

    def retranslateUi(self, mainMenu):
        mainMenu.setWindowTitle(QCoreApplication.translate("mainMenu", u"ReLuu", None))
        self.logo_mainMenu.setText("")
#if QT_CONFIG(tooltip)
        self.start_model_button.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.start_model_button.setText(QCoreApplication.translate("mainMenu", u"Start", None))
        self.feedback_button.setText(QCoreApplication.translate("mainMenu", u"Submit Feedback", None))
        self.sign_out_button.setText(QCoreApplication.translate("mainMenu", u"Exit", None))
    # retranslateUi

