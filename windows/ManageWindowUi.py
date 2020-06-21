# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ManageWindowUi.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        self.menuStart = QtWidgets.QMenu(self.menubar)
        self.menuStart.setObjectName("menuStart")
        self.menuSave = QtWidgets.QMenu(self.menubar)
        self.menuSave.setObjectName("menuSave")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionBrute = QtWidgets.QAction(MainWindow)
        self.actionBrute.setObjectName("actionBrute")
        self.actionEvoDAP = QtWidgets.QAction(MainWindow)
        self.actionEvoDAP.setObjectName("actionEvoDAP")
        self.actionAboutNetwork = QtWidgets.QAction(MainWindow)
        self.actionAboutNetwork.setObjectName("actionAboutNetwork")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.actionAboutAuthors = QtWidgets.QAction(MainWindow)
        self.actionAboutAuthors.setObjectName("actionAboutAuthors")
        self.actionEvoDDAP = QtWidgets.QAction(MainWindow)
        self.actionEvoDDAP.setObjectName("actionEvoDDAP")
        self.actionSaveBrute = QtWidgets.QAction(MainWindow)
        self.actionSaveBrute.setObjectName("actionSaveBrute")
        self.actionSaveEvoDAP = QtWidgets.QAction(MainWindow)
        self.actionSaveEvoDAP.setObjectName("actionSaveEvoDAP")
        self.actionSaveEvoDDAP = QtWidgets.QAction(MainWindow)
        self.actionSaveEvoDDAP.setObjectName("actionSaveEvoDDAP")
        self.menuStart.addAction(self.actionBrute)
        self.menuStart.addAction(self.actionEvoDAP)
        self.menuStart.addAction(self.actionEvoDDAP)
        self.menuSave.addAction(self.actionSaveBrute)
        self.menuSave.addAction(self.actionSaveEvoDAP)
        self.menuSave.addAction(self.actionSaveEvoDDAP)
        self.menubar.addAction(self.menuStart.menuAction())
        self.menubar.addAction(self.menuSave.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OAST"))
        self.menuStart.setTitle(_translate("MainWindow", "Start"))
        self.menuSave.setTitle(_translate("MainWindow", "Save"))
        self.actionBrute.setText(_translate("MainWindow", "Brute force (DAP and DDAP)"))
        self.actionEvoDAP.setText(_translate("MainWindow", "Evolutionary algorithm (DAP)"))
        self.actionAboutNetwork.setText(_translate("MainWindow", "About network"))
        self.action.setText(_translate("MainWindow", "About algorithms"))
        self.actionAboutAuthors.setText(_translate("MainWindow", "About authors"))
        self.actionEvoDDAP.setText(_translate("MainWindow", "Evolutionary algorithm (DDAP)"))
        self.actionSaveBrute.setText(_translate("MainWindow", "Brute force solution"))
        self.actionSaveEvoDAP.setText(_translate("MainWindow", "Evolutionary DAP solution"))
        self.actionSaveEvoDDAP.setText(_translate("MainWindow", "Evolutionary DDAP solution"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
