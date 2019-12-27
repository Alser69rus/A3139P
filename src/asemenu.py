from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
import typing


class MenuItem(QtWidgets.QPushButton):
    entered = pyqtSignal()
    NONE = 0
    NORMAL = 1
    SUCCESS = 2
    FAIL = 3

    def __init__(self, *args):
        super().__init__(*args)
        self._selected: bool = False
        self._state: int = self.NORMAL

        self.setFlat(True)
        self.setFont(QtGui.QFont('Segoi Ui', 16))
        self.setMouseTracking(True)
        self.setIconSize(QtCore.QSize(32, 32))
        self.set_style()

    def enterEvent(self, QEvent) -> None:
        self.entered.emit()

    @property
    def active(self) -> bool:
        return self.isVisible() and self.isEnabled()

    @property
    def selected(self) -> bool:
        return self._selected

    @selected.setter
    def selected(self, value: bool):
        self._selected = value
        self.set_style()

    @property
    def state(self) -> int:
        return self._state

    @state.setter
    def state(self, value: int) -> None:
        self._state: int = value
        self.set_style()

    def set_style(self) -> None:
        if self.state == self.NORMAL:
            color: str = 'rgba(10,10,10,0%)'
            pressed_color: str = 'rgba(30,0,0,30%)'
            icon = QtGui.QIcon('img/menu_item_normal.png')
        elif self.state == self.SUCCESS:
            color: str = 'rgba(0,200,0,10%)'
            pressed_color: str = 'rgba(30,0,0,30%)'
            icon = QtGui.QIcon('img/menu_item_success.png')
        elif self.state == self.FAIL:
            color: str = 'rgba(200,0,0,10%)'
            pressed_color: str = 'rgba(30,0,0,30%)'
            icon = QtGui.QIcon('img/menu_item_fail.png')
        else:
            color: str = 'rgba(10,10,10,0%)'
            pressed_color: str = 'rgba(30,0,0,30%)'
            icon = QtGui.QIcon()

        if self.selected:
            border_style: str = 'solid'
        else:
            border_style: str = 'none'

        style: str = f'QPushButton' \
                     f'{{' \
                     f'border:2px; ' \
                     f'border-radius:8px; ' \
                     f'border-color:black; ' \
                     f'text-align:left; ' \
                     f'padding: 8px; ' \
                     f'background-color:{color};' \
                     f'border-style:{border_style};' \
                     f'}} ' \
                     f' QPushButton:pressed' \
                     f'{{' \
                     f'background-color:{pressed_color}' \
                     f'}}'

        self.setStyleSheet(style)
        self.setIcon(icon)


class MenuCaption(QtWidgets.QLabel):
    def __init__(self, text: str, *args):
        super().__init__(text, *args)
        self.setFont(QtGui.QFont('Segoi Ui', 32))
        self.setText(text)
        self.setAlignment(QtCore.Qt.AlignHCenter)


class Menu(QtWidgets.QWidget):
    def __init__(self, parent=None, caption: str = '', *args):
        super().__init__(parent, *args)
        self.onBack: typing.Optional[typing.Callable] = None
        self.caption = MenuCaption(caption)
        self.items: typing.List[MenuItem] = []
        self.current: MenuItem = None
        self.vbox = QtWidgets.QVBoxLayout()
        self.setLayout(self.vbox)
        self.vbox.addWidget(self.caption)
        self.vbox.addSpacing(40)
        self.first()

    def addMenuItem(self, item: MenuItem) -> MenuItem:
        self.items.append(item)
        self.vbox.addWidget(item)
        item.entered.connect(self.onEnter)
        return item
		

    def onEnter(self) -> None:
        item: MenuItem = self.sender()
        self.select(item)

    def select(self, item: MenuItem) -> bool:
        if not item.active:
            return False
        if not (self.current is None):
            self.current.selected = False
        self.current: MenuItem = item
        self.current.selected = True
        return True

    @QtCore.pyqtSlot()
    def first(self) -> None:
        for item in self.items:
            if self.select(item): return

    @QtCore.pyqtSlot()
    def next(self) -> None:
        if self.current is None:
            self.first()
            return
        i: int = self.items.index(self.current)
        l: int = len(self.items)
        for _ in range(l):
            i += 1
            if i >= l:
                i -= l
            if self.select(self.items[i]): return

    @QtCore.pyqtSlot()
    def previos(self) -> None:
        if self.current is None:
            self.last()
            return
        i: int = self.items.index(self.current)
        l: int = len(self.items)
        for _ in range(l):
            i -= 1
            if i < 0:
                i += l
            if self.select(self.items[i]): return

    @QtCore.pyqtSlot()
    def last(self) -> None:
        l: int = len(self.items)
        for i in range(l - 1, -1, -1):
            if self.select(self.items[i]): return

    @QtCore.pyqtSlot()
    def accept(self) -> None:
        if self.current is None:
            return
        self.current.animateClick()

    @QtCore.pyqtSlot()
    def back(self) -> None:
        if not (self.onBack is None):
            self.onBack()

    def reset(self) -> None:
        for item in self.items:
            item.state = item.NORMAL
        self.first()


class StackedMenu(QtWidgets.QWidget):
    up_clicked = QtCore.pyqtSignal()
    down_clicked = QtCore.pyqtSignal()
    ok_clicked = QtCore.pyqtSignal()
    back_clicked = QtCore.pyqtSignal()

    def __init__(self, *args):
        super().__init__(*args)
        self.tabs = QtWidgets.QStackedLayout()
        self.setLayout(self.tabs)
        self._current: typing.Optional[Menu] = None

    def addMenu(self, menu: Menu) -> None:
        self.tabs.addWidget(menu)
        if self.current is None:
            self.current = menu

    @property
    def current(self) -> Menu:
        return self._current

    @current.setter
    def current(self, value: Menu):
        self.disconnect_menu(self.current)
        self.tabs.setCurrentWidget(value)
        self._current = value
        self.connect_menu(value)

    def set_current(self, value: Menu):
        self.current = value

    def disconnect_menu(self, menu: Menu) -> None:
        if not (menu is None):
            self.up_clicked.disconnect(menu.previos)
            self.down_clicked.disconnect(menu.next)
            self.ok_clicked.disconnect(menu.accept)
            self.back_clicked.disconnect(menu.back)

    def connect_menu(self, menu: Menu) -> None:
        if not (menu is None):
            self.up_clicked.connect(menu.previos)
            self.down_clicked.connect(menu.next)
            self.ok_clicked.connect(menu.accept)
            self.back_clicked.connect(menu.back)
