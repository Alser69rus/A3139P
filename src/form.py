# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 768)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        MainWindow.setFont(font)
        MainWindow.setMouseTracking(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.vbox = QtWidgets.QVBoxLayout(self.centralwidget)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(0)
        self.vbox.setObjectName("vbox")
        self.manometers = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manometers.sizePolicy().hasHeightForWidth())
        self.manometers.setSizePolicy(sizePolicy)
        self.manometers.setMinimumSize(QtCore.QSize(0, 150))
        self.manometers.setObjectName("manometers")
        self.vbox.addWidget(self.manometers)
        self.table = QtWidgets.QWidget(self.centralwidget)
        self.table.setObjectName("table")
        self.hbox = QtWidgets.QHBoxLayout(self.table)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(0)
        self.hbox.setObjectName("hbox")
        self.menu = StackedMenu(self.table)
        self.menu.setObjectName("menu")
        self.hbox.addWidget(self.menu)
        self.text = QtWidgets.QLabel(self.table)
        self.text.setFrameShape(QtWidgets.QFrame.Box)
        self.text.setObjectName("text")
        self.hbox.addWidget(self.text)
        self.img = QtWidgets.QLabel(self.table)
        self.img.setFrameShape(QtWidgets.QFrame.Box)
        self.img.setObjectName("img")
        self.hbox.addWidget(self.img)
        self.graph = QtWidgets.QWidget(self.table)
        self.graph.setObjectName("graph")
        self.hbox.addWidget(self.graph)
        self.vbox.addWidget(self.table)
        self.btn_panel = BtnPanel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_panel.sizePolicy().hasHeightForWidth())
        self.btn_panel.setSizePolicy(sizePolicy)
        self.btn_panel.setMinimumSize(QtCore.QSize(0, 40))
        self.btn_panel.setObjectName("btn_panel")
        self.vbox.addWidget(self.btn_panel)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 31))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.btn_panel.back_clicked.connect(self.menu.back_clicked)
        self.btn_panel.down_clicked.connect(self.menu.down_clicked)
        self.btn_panel.up_clicked.connect(self.menu.up_clicked)
        self.btn_panel.yes_clicked.connect(self.menu.ok_clicked)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "А3139 Стенд испытания пневматики"))
        self.text.setText(_translate("MainWindow", "TextLabel"))
        self.img.setText(_translate("MainWindow", "TextLabel"))

from src.asemenu import StackedMenu
from src.btnpanel import BtnPanel
