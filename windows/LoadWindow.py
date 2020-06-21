from PyQt5 import QtWidgets, QtCore
from windows import LoadWindowUi
import tools.parser


class LoadWindow(QtWidgets.QMainWindow):

    switchToManage = QtCore.pyqtSignal(object)  # object is a list of networks

    def __init__(self):
        super(LoadWindow, self).__init__()

        self.network = None

        self.ui = LoadWindowUi.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        self.ui.errorDialog = QtWidgets.QErrorMessage()

        self.ui.loadButton.clicked.connect(self._loadFile)

        self.ui.startButton.clicked.connect(self.start)

        # debug = "/run/user/1000/doc/40900f4a/net12_1.txt"
        # debug = "/run/user/1000/doc/f196f992/net4.txt"
        # self.ui.loadLine.setText(debug)

    def _loadFile(self):
        temp = QtWidgets.QFileDialog.getOpenFileName(self, caption='Select file', directory="./nets", filter='Text files (*.txt)')[0]  # getOpen... returns tuple
        if temp != "":
            self.ui.loadLine.setText(temp)

    def start(self):
        path = self.ui.loadLine.text()
        pars = tools.parser.Parser(self.ui.errorDialog)

        # try:
        #     networks, logger = topoMaker.createTopology(self.topoOptions, self.ui.error_dialog)
        # except BaseException as e:
        #     self.ui.error_dialog.showMessage('Topology creation was unsuccessful. Exception: ' + str(e))
        #     return
        self.network = pars.parseFile(path)

        if not self.network:
            #self.ui.error_dialog.showMessage('ERROR: Network not created.')
            return

        self.switchToManage.emit(self.network)
