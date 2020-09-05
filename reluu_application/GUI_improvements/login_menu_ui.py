

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(470, 418)
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        MainWindow.setPalette(palette)
        MainWindow.setStyleSheet(u"QLineEdit {\n"
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
"background-color: #e1fbff\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.logo_vbox = QVBoxLayout()
        self.logo_vbox.setObjectName(u"logo_vbox")
        self.logo_vbox.setSizeConstraint(QLayout.SetMaximumSize)
        self.logo_vbox.setContentsMargins(-1, -1, -1, 7)
        self.logo = QLabel(self.centralwidget)
        self.logo.setObjectName(u"logo")
        self.logo.setMaximumSize(QSize(150, 150))
        self.logo.setPixmap(QPixmap("reluu_application/GUI_improvements/logo_transparent_background.png"))
        self.logo.setScaledContents(True)
        self.logo.setAlignment(Qt.AlignCenter)

        self.logo_vbox.addWidget(self.logo, 0, Qt.AlignHCenter)

        self.Sign_in_title = QHBoxLayout()
        self.Sign_in_title.setObjectName(u"Sign_in_title")
        self.Sign_in_title.setSizeConstraint(QLayout.SetMinimumSize)
        self.Sign_in_title.setContentsMargins(75, 0, 70, -1)
        self.sign_in = QLabel(self.centralwidget)
        self.sign_in.setObjectName(u"sign_in")
        self.sign_in.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setFamily(u"Segoe UI Symbol")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.sign_in.setFont(font)
        self.sign_in.setAlignment(Qt.AlignCenter)

        self.Sign_in_title.addWidget(self.sign_in)


        self.logo_vbox.addLayout(self.Sign_in_title)


        self.verticalLayout.addLayout(self.logo_vbox)

        self.email_pw_vbox = QVBoxLayout()
        self.email_pw_vbox.setSpacing(20)
        self.email_pw_vbox.setObjectName(u"email_pw_vbox")
        self.email_pw_vbox.setContentsMargins(75, 0, 70, -1)
        self.password_input = QLineEdit(self.centralwidget)
        self.password_input.setObjectName(u"password_input")
        font1 = QFont()
        font1.setPointSize(12)
        self.password_input.setFont(font1)

        self.email_pw_vbox.addWidget(self.password_input)

        self.email_input = QLineEdit(self.centralwidget)
        self.email_input.setObjectName(u"email_input")
        self.email_input.setEnabled(True)
        self.email_input.setFont(font1)

        self.email_pw_vbox.addWidget(self.email_input)

        self.sign_in_button_hbox = QHBoxLayout()
        self.sign_in_button_hbox.setSpacing(10)
        self.sign_in_button_hbox.setObjectName(u"sign_in_button_hbox")
        self.keep_signed_in = QCheckBox(self.centralwidget)
        self.keep_signed_in.setObjectName(u"keep_signed_in")
        font2 = QFont()
        font2.setFamily(u"Segoe UI Symbol")
        font2.setPointSize(10)
        self.keep_signed_in.setFont(font2)

        self.sign_in_button_hbox.addWidget(self.keep_signed_in)

        self.Sign_in_button = QPushButton(self.centralwidget)
        self.Sign_in_button.setObjectName(u"Sign_in_button")
        self.Sign_in_button.setMinimumSize(QSize(75, 35))
        self.Sign_in_button.setMaximumSize(QSize(75, 35))
        self.Sign_in_button.setFont(font)

        self.sign_in_button_hbox.addWidget(self.Sign_in_button)


        self.email_pw_vbox.addLayout(self.sign_in_button_hbox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.forgot_password = QLabel(self.centralwidget)
        self.forgot_password.setObjectName(u"forgot_password")
        font3 = QFont()
        font3.setFamily(u"Segoe UI Symbol")
        font3.setPointSize(9)
        self.forgot_password.setFont(font3)

        self.horizontalLayout_2.addWidget(self.forgot_password)

        self.sign_up_free = QLabel(self.centralwidget)
        self.sign_up_free.setObjectName(u"sign_up_free")
        self.sign_up_free.setFont(font3)
        self.sign_up_free.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.sign_up_free)


        self.email_pw_vbox.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addLayout(self.email_pw_vbox)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.logo.setText("")
        self.sign_in.setText(QCoreApplication.translate("MainWindow", u"Sign In", None))
        self.password_input.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter your password", None))
        self.email_input.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter your email", None))
        self.keep_signed_in.setText(QCoreApplication.translate("MainWindow", u"Keep me signed in", None))
        self.Sign_in_button.setText(QCoreApplication.translate("MainWindow", u"Sign In", None))
        self.forgot_password.setText(QCoreApplication.translate("MainWindow", u"Forgot Password?", None))
        self.sign_up_free.setText(QCoreApplication.translate("MainWindow", u"Sign Up Free", None))
    # retranslateUi