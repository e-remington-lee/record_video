# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_menu.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

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
        self.logo_mainMenu.setPixmap(QPixmap(u"logo_transparent_background.png"))
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

        self.button_layout.addWidget(self.start_model_button)

        self.sign_out_button = QPushButton(mainMenu)
        self.sign_out_button.setObjectName(u"sign_out_button")
        font1 = QFont()
        font1.setFamily(u"Segoe UI Symbol")
        font1.setPointSize(14)
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
        self.start_model_button.setText(QCoreApplication.translate("mainMenu", u"Start", None))
        self.sign_out_button.setText(QCoreApplication.translate("mainMenu", u"Exit", None))
    # retranslateUi

