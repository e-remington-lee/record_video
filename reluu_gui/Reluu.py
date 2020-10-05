import os
import sys
import multiprocessing
import importlib.util
import webbrowser

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


from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
from login_menu_qtd import Ui_MainWindow
from main_menu_qtd import Ui_mainMenu
import grab_image

# class LoginWindow(QtWidgets.QWidget, Ui_MainWindow):
#     def __init__(self, *args, **kwargs):
#         super(LoginWindow, self).__init__(*args, **kwargs)
#         self.setWindowTitle('ReLuu')
#         self.setupUi(self)
#         icon = QtGui.QIcon("reluu_application/GUI_improvements/logo_transparent_background.png")
#         self.setWindowIcon(icon)
    
#         self.Sign_in_button.clicked.connect(lambda: self.sign_in_1(self.email_input.text(), self.password_input.text()))

#     def sign_in_1(self, email, password):
#         if email == "1" and password == "1":
#             if self.keep_signed_in.isChecked():
#                 print("staying signed in")
#             self.close()
#             self.main_menu = MainMenu()
#             self.main_menu.show()
#         else:
#             print("failed to login")     


class MainMenu(QtWidgets.QWidget, Ui_mainMenu):
    def __init__(self, *args, **kwargs):
        super(MainMenu, self).__init__(*args, **kwargs)
        self.setWindowTitle('ReLuu')
        self.setupUi(self)
        cur_dir = os.getcwd()
        # os.chdir(sys._MEIPASS)
        icon = QtGui.QIcon("auxiliary_files\\logo_transparent_background.png")
        self.setWindowIcon(icon)
        os.chdir(cur_dir)

        self.start_model_button.clicked.connect(self.start_model)
        self.sign_out_button.clicked.connect(self.logout)
        self.abc = grab_image.GrabImage()

    def start_model(self):
        # webbrowser.open("http://google.com")
        self.close()
        self.abc.start_grab()

    
    def logout(self):
        self.close()
        # self.login = LoginWindow()
        # self.login.show()

        
if __name__ == "__main__":
    # multiprocessing.freeze_support()
    app = QtWidgets.QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec_())
