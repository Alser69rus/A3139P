from PyQt5 import QtCore, QtWidgets
from typing import List


class MenuComponent:
    def __init__(self, text: str):
        self.text: str = text
        self.parent: 'MenuComponent' = None
        self.children: List['MenuComponent'] = []

    def add(self, component: 'MenuComponent') -> 'MenuComponent':
        pass

    def remove(self, component: 'MenuComponent') -> None:
        pass

    @staticmethod
    def is_menu() -> bool:
        return False


class Menu(MenuComponent):
    def __init__(self, text: str):
        super().__init__(text)
        self.caption: str = text

    def add(self, component: MenuComponent) -> MenuComponent:
        self.children.append(component)
        component.parent = self
        return component

    def remove(self, component: MenuComponent) -> None:
        self.children.remove(component)
        component.parent = None

    @staticmethod
    def is_menu():
        return True


class Button(MenuComponent):
    pass


class MenuController(QtCore.QObject):
    def __init__(self, parent=None, widget: QtWidgets.QWidget = None):
        super().__init__(parent=parent)
        self.model: MenuComponent = None
        self.view: QtWidgets.QWidget = widget

        self.init_menu()
        self.create_view()

    def init_menu(self):
        pass

    def create_view(self):
        self.view.stl = QtWidgets.QStackedLayout()
        self.view.setLayout(self.view.stl)


