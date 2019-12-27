from unittest import TestCase
from PyQt5 import QtTest, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from src.menu import Menu, Button, MenuController


class Test(TestCase):
    def setUp(self):
        app = QtWidgets.QApplication([])
        self.widget = QtWidgets.QWidget()
        self.mc = MC(parent=None, widget=self.widget)

    def test_menu_init(self):
        self.assertEqual(self.widget, self.mc.view)

    def test_parent(self):
        self.assertIsNone(self.mc.model.parent)
        self.assertEqual(self.mc.m1.parent, self.mc.model)
        self.assertEqual(self.mc.b1.parent, self.mc.model)
        self.assertEqual(self.mc.b2.parent, self.mc.m1)

    def test_child(self):
        self.assertEqual(self.mc.model.children, [self.mc.m1, self.mc.b1])
        self.assertEqual(self.mc.m1.children, [self.mc.b2])
        self.assertEqual(self.mc.b1.children, [])
        self.assertEqual(self.mc.b2.children, [])

    def test_is_menu(self):
        self.assertTrue(self.mc.model.is_menu())
        self.assertTrue(self.mc.m1.is_menu())
        self.assertFalse(self.mc.b1.is_menu())
        self.assertFalse(self.mc.b2.is_menu())

    def test_text(self):
        self.assertEqual(self.mc.model.text, 'Main')
        self.assertEqual(self.mc.model.caption, 'Main')
        self.assertEqual(self.mc.m1.text, 'Menu 1')
        self.assertEqual(self.mc.m1.caption, 'Menu One')
        self.assertEqual(self.mc.b1.text, 'Exit')
        self.assertEqual(self.mc.b2.text, 'Back')


class MC(MenuController):
    def init_menu(self):
        self.model = Menu('Main')
        self.m1 = self.model.add(Menu('Menu 1'))
        self.b1 = self.model.add(Button('Exit'))

        self.m1.caption = 'Menu One'
        self.b2 = self.m1.add(Button('Back'))
