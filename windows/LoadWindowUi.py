# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoadWindowUi.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(502, 254)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.loadLine = QtWidgets.QLineEdit(self.centralwidget)
        self.loadLine.setGeometry(QtCore.QRect(10, 120, 481, 31))
        self.loadLine.setObjectName("loadLine")
        self.loadButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadButton.setGeometry(QtCore.QRect(360, 80, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.loadButton.setFont(font)
        self.loadButton.setObjectName("loadButton")
        self.titlelLabel = QtWidgets.QLabel(self.centralwidget)
        self.titlelLabel.setGeometry(QtCore.QRect(10, 12, 481, 41))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.titlelLabel.setFont(font)
        self.titlelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titlelLabel.setObjectName("titlelLabel")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(100, 170, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.startButton.setFont(font)
        self.startButton.setObjectName("startButton")
        self.textLabel = QtWidgets.QLabel(self.centralwidget)
        self.textLabel.setGeometry(QtCore.QRect(10, 90, 281, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textLabel.setFont(font)
        self.textLabel.setObjectName("textLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 502, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OAST"))
        self.loadButton.setText(_translate("MainWindow", "Load"))
        self.titlelLabel.setText(_translate("MainWindow", "OAST - Optimalization project"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.textLabel.setText(_translate("MainWindow", "Select file with network configuration:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
