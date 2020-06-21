#!/usr/bin/python3

from PyQt5 import QtWidgets
from windows import LoadWindow
from windows import ManageWindow
import sys


class Program:

    def __init__(self):
        self.loadWindow = None
        self.manageWindow = None

    def start(self):
        self._showLoadWindow()

    def _showLoadWindow(self):
        if self.loadWindow is None:
            self.loadWindow = LoadWindow.LoadWindow()
        self.loadWindow.switchToManage.connect(self._showManageWindow)  # signal passes list of networks
        self.loadWindow.show()

    def _showManageWindow(self, network):
        if self.manageWindow is None:
            self.manageWindow = ManageWindow.ManageWindow(network)
        self.loadWindow.close()
        self.manageWindow.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    program = Program()
    program.start()
    sys.exit(app.exec())
