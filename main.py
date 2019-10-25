import sys
from PyQt5 import QtWidgets
from src.form import Ui_MainWindow
from src.mainmenu import Ui_MainMenu


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow, Ui_MainMenu):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setupMenu(self)
        self.img.setVisible(False)
        self.graph.setVisible(False)
        self.text.setVisible(False)
        self.manometers.setVisible(False)
        self.btn_panel.set_btn_visible('back up yes down')



app = QtWidgets.QApplication(sys.argv)
frm = MainWindow()

frm.show()
print(frm.width(), frm.height())
sys.exit(app.exec_())
