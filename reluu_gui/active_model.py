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


class Ui_active_model(object):
    def setupUi(self, active_model):
        if not active_model.objectName():
            active_model.setObjectName(u"active_model")
        active_model.resize(300, 510)
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        active_model.setPalette(palette)
        active_model.setStyleSheet(u"QLineEdit {\n"
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
        self.verticalLayout_2 = QVBoxLayout(active_model)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.active_model_layout = QVBoxLayout()
        self.active_model_layout.setObjectName(u"active_model_layout")
        self.icon_layout = QVBoxLayout()
        self.icon_layout.setObjectName(u"icon_layout")
        self.emotion_icon_layout = QVBoxLayout()
        self.emotion_icon_layout.setObjectName(u"emotion_icon_layout")
        self.emotion_icon_layout.setSizeConstraint(QLayout.SetFixedSize)

        self.icon_layout.addLayout(self.emotion_icon_layout)

        self.warning_layout = QVBoxLayout()
        self.warning_layout.setSpacing(0)
        self.warning_layout.setObjectName(u"warning_layout")
        self.warning_layout.setSizeConstraint(QLayout.SetMaximumSize)
        self.warning_layout.setContentsMargins(-1, 7, -1, 0)
        self.warning_label1 = QLabel(active_model)
        self.warning_label1.setObjectName(u"warning_label1")
        self.warning_label1.setMaximumSize(QSize(166666, 15))
        palette1 = QPalette()
        brush1 = QBrush(QColor(214, 0, 0, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.WindowText, brush1)
        brush2 = QBrush(QColor(218, 0, 0, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Text, brush2)
        brush3 = QBrush(QColor(255, 0, 0, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.ToolTipText, brush3)
        palette1.setBrush(QPalette.Inactive, QPalette.WindowText, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Text, brush2)
        palette1.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush3)
        brush4 = QBrush(QColor(120, 120, 120, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Disabled, QPalette.WindowText, brush4)
        palette1.setBrush(QPalette.Disabled, QPalette.Text, brush4)
        palette1.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush3)
        self.warning_label1.setPalette(palette1)
        font = QFont()
        font.setFamily(u"Segoe UI Symbol")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.warning_label1.setFont(font)
        self.warning_label1.setScaledContents(False)
        self.warning_label1.setAlignment(Qt.AlignCenter)
        self.warning_label1.setWordWrap(False)

        self.warning_layout.addWidget(self.warning_label1)

        self.warning_label2 = QLabel(active_model)
        self.warning_label2.setObjectName(u"warning_label2")
        self.warning_label2.setMaximumSize(QSize(166666, 21))
        palette2 = QPalette()
        palette2.setBrush(QPalette.Active, QPalette.WindowText, brush1)
        palette2.setBrush(QPalette.Inactive, QPalette.WindowText, brush1)
        palette2.setBrush(QPalette.Disabled, QPalette.WindowText, brush4)
        self.warning_label2.setPalette(palette2)
        font1 = QFont()
        font1.setFamily(u"Segoe UI Symbol")
        self.warning_label2.setFont(font1)
        self.warning_label2.setAlignment(Qt.AlignCenter)

        self.warning_layout.addWidget(self.warning_label2)


        self.icon_layout.addLayout(self.warning_layout)

        self.detailed_view_layout = QVBoxLayout()
        self.detailed_view_layout.setObjectName(u"detailed_view_layout")
        self.detailed_view_layout.setSizeConstraint(QLayout.SetMaximumSize)
        self.detailed_view_checkbox = QCheckBox(active_model)
        self.detailed_view_checkbox.setObjectName(u"detailed_view_checkbox")
        self.detailed_view_checkbox.setFont(font1)
        self.detailed_view_checkbox.setChecked(False)

        self.detailed_view_layout.addWidget(self.detailed_view_checkbox, 0, Qt.AlignHCenter)


        self.icon_layout.addLayout(self.detailed_view_layout)


        self.active_model_layout.addLayout(self.icon_layout)

        self.button_layout = QHBoxLayout()
        self.button_layout.setObjectName(u"button_layout")
        self.button_layout.setContentsMargins(50, 7, 50, -1)
        self.stop_session_button = QPushButton(active_model)
        self.stop_session_button.setObjectName(u"stop_session_button")
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(True)
        font2.setWeight(75)
        self.stop_session_button.setFont(font2)

        self.button_layout.addWidget(self.stop_session_button)


        self.active_model_layout.addLayout(self.button_layout)


        self.verticalLayout_2.addLayout(self.active_model_layout)


        self.retranslateUi(active_model)

        QMetaObject.connectSlotsByName(active_model)
    # setupUi

    def retranslateUi(self, active_model):
        active_model.setWindowTitle(QCoreApplication.translate("active_model", u"ReLuu", None))
        self.warning_label1.setText(QCoreApplication.translate("active_model", u"No Face Detected", None))
        self.warning_label2.setText(QCoreApplication.translate("active_model", u"Resize or Move the Face Box", None))
        self.detailed_view_checkbox.setText(QCoreApplication.translate("active_model", u"Show Detailed View", None))
        self.stop_session_button.setText(QCoreApplication.translate("active_model", u"Stop", None))
    # retranslateUi

