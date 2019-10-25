from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot


class BtnPanel(QtWidgets.QWidget):
    yes_clicked = pyqtSignal()
    no_clicked = pyqtSignal()
    up_clicked = pyqtSignal()
    down_clicked = pyqtSignal()
    run_clicked = pyqtSignal()
    back_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.key_up = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Up), self)
        self.key_up.activated.connect(self.on_up_clicked)
        self.key_down = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Down), self)
        self.key_down.activated.connect(self.on_down_clicked)
        self.key_yes = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return), self)
        self.key_yes.activated.connect(self.on_yes_clicked)
        self.key_no = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Space), self)
        self.key_no.activated.connect(self.on_no_clicked)
        self.key_back = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self)
        self.key_back.activated.connect(self.on_back_clicked)

        self.style: str = 'QPushButton' \
                          '{' \
                          'border:2px;' \
                          'border-radius:8px;' \
                          'border-color:black;' \
                          'text-align:center;' \
                          'padding: 4px;' \
                          'background-color:rgba(10,10,10,10%);' \
                          'border-style:none;' \
                          'font:20px "Segoi UI";' \
                          'min-width:80px;' \
                          'icon-size: 32px 32px' \
                          '}' \
                          ' QPushButton:pressed' \
                          '{' \
                          'background-color:rgba(30,0,0,30%)' \
                          '}'

        self.setStyleSheet(self.style)

        self.hbox = QtWidgets.QHBoxLayout()
        self.btn_back = QtWidgets.QPushButton('Назад')
        self.btn_up = QtWidgets.QPushButton('Вверх')
        self.btn_down = QtWidgets.QPushButton('Вниз')
        self.btn_yes = QtWidgets.QPushButton('Да')
        self.btn_no = QtWidgets.QPushButton('Нет')
        self.btn_run = QtWidgets.QPushButton('Запуск')

        self.btn_back.setIcon(QtGui.QIcon('img/btn_panel_back.png'))
        self.btn_up.setIcon(QtGui.QIcon('img/btn_panel_up.png'))
        self.btn_down.setIcon(QtGui.QIcon('img/btn_panel_down.png'))
        self.btn_yes.setIcon(QtGui.QIcon('img/btn_panel_yes.png'))
        self.btn_no.setIcon(QtGui.QIcon('img/btn_panel_no.png'))
        self.btn_run.setIcon(QtGui.QIcon('img/btn_panel_run.png'))

        self.hbox.addWidget(self.btn_back)
        self.hbox.addWidget(self.btn_up)
        self.hbox.addWidget(self.btn_down)
        self.hbox.addWidget(self.btn_yes)
        self.hbox.addWidget(self.btn_no)
        self.hbox.addWidget(self.btn_run)

        self.btn_back.clicked.connect(self.back_clicked)
        self.btn_run.clicked.connect(self.run_clicked)
        self.btn_no.clicked.connect(self.no_clicked)
        self.btn_yes.clicked.connect(self.yes_clicked)
        self.btn_up.clicked.connect(self.up_clicked)
        self.btn_down.clicked.connect(self.down_clicked)

        self.btn_no.setVisible(False)
        self.btn_run.setVisible(False)

        self.setLayout(self.hbox)

    @pyqtSlot()
    def on_yes_clicked(self) -> None:
        self.btn_clicked(self.btn_yes)

    @pyqtSlot()
    def on_no_clicked(self) -> None:
        self.btn_clicked(self.btn_no)

    @pyqtSlot()
    def on_up_clicked(self) -> None:
        self.btn_clicked(self.btn_up)

    @pyqtSlot()
    def on_down_clicked(self) -> None:
        self.btn_clicked(self.btn_down)

    @pyqtSlot()
    def on_back_clicked(self) -> None:
        self.btn_clicked(self.btn_back)

    @pyqtSlot()
    def on_run_clicked(self) -> None:
        self.btn_clicked(self.btn_run)

    @staticmethod
    def btn_clicked(btn: QtWidgets.QPushButton) -> None:
        if btn.isVisible() and btn.isEnabled():
            btn.animateClick()

    def set_btn_visible(self, btns: str):
        btns = btns.lower()
        self.btn_yes.setVisible(btns.find('yes') >= 0)
        self.btn_no.setVisible(btns.find('no') >= 0)
        self.btn_back.setVisible(btns.find('back') >= 0)
        self.btn_run.setVisible(btns.find('run') >= 0)
        self.btn_up.setVisible(btns.find('up') >= 0)
        self.btn_down.setVisible(btns.find('down') >= 0)
