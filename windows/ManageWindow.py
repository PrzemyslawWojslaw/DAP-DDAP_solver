from PyQt5 import QtWidgets, QtCore
from windows import ManageWindowUi
from algorithms.brute import BruteForceSolver
from algorithms.evolutionary import EvolutionarySolver
from threading import Thread
import tools.serializer
import tools.logger


class EvoInputDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.seed = QtWidgets.QLineEdit(self)
        self.seed.setText("None")
        self.initial_population_size = QtWidgets.QLineEdit(self)
        self.initial_population_size.setText("10")
        self.number_of_offsprings = QtWidgets.QLineEdit(self)
        self.number_of_offsprings.setText("2")
        self.crossover_prob = QtWidgets.QLineEdit(self)
        self.crossover_prob.setText("0.1")
        self.mutation_prob = QtWidgets.QLineEdit(self)
        self.mutation_prob.setText("0.1")
        self.criterion_type = QtWidgets.QLineEdit(self)
        self.criterion_type.setText("time")
        self.criterion_value = QtWidgets.QLineEdit(self)
        self.criterion_value.setText("3")
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self)

        layout = QtWidgets.QFormLayout(self)
        layout.addRow("Seed (\"None\" or integer)", self.seed)
        layout.addRow("Initial population size (integer)", self.initial_population_size)
        layout.addRow("Number of offsprings (even integer)", self.number_of_offsprings)
        layout.addRow("Probability of crossover (float)", self.crossover_prob)
        layout.addRow("Probability of mutation (float)", self.mutation_prob)
        layout.addRow("Criterion type \n- \"time\"\n- \"number_of_generations\"\n- \"number_of_mutations\"\n- \"lack_of_improvement\"", self.criterion_type)
        layout.addRow("Criterion value (integer)", self.criterion_value)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInput(self):
        if self.seed.text() == "None":
            seed = None
        else:
            seed = int(self.seed.text())
        initial_population_size = int(self.initial_population_size.text())
        number_of_offsprings = int(self.number_of_offsprings.text())
        crossover_prob = float(self.crossover_prob.text())
        mutation_prob = float(self.mutation_prob.text())
        criterion = (self.criterion_type.text(), int(self.criterion_value.text()))
        return seed, initial_population_size, number_of_offsprings, crossover_prob, mutation_prob, criterion


class SaveInputDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, brute=True, max_value=0):
        super().__init__(parent)

        if brute:
            question_text = "Select ID of a solution (from 1 to " + str(max_value) + ") or \"bestDAP\" / \"bestDDAP\":"
            default_answer = "bestDDAP"
        else:
            question_text = "Select generation to save its best solution (from 1 to " + str(max_value) + ") or \"best\":"
            default_answer = "best"

        self.answer = QtWidgets.QLineEdit(self)
        self.answer.setText(default_answer)
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self)

        layout = QtWidgets.QFormLayout(self)
        layout.addRow(question_text, self.answer)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInput(self):
        answer = self.answer.text()
        return answer


class ManageWindow(QtWidgets.QMainWindow):

    def __init__(self, network):
        super(ManageWindow, self).__init__()

        self.network = network
        self.logger = tools.logger.Logger(self.network.name)

        self.ui = ManageWindowUi.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.errorDialog = QtWidgets.QErrorMessage()

        self.bruteForceSolver = BruteForceSolver(self.ui.errorDialog, self.logger, self.network)
        self.evolutionarySolver = EvolutionarySolver(self.ui.errorDialog, self.logger, self.network)

        self._prepareLayout()

        self.ui.actionBrute.triggered.connect(self._prepareBrute)
        self.ui.actionEvoDAP.triggered.connect(lambda: self._prepareEvolutionary(ddap=False))
        self.ui.actionEvoDDAP.triggered.connect(lambda: self._prepareEvolutionary(ddap=True))

        self.ui.actionSaveBrute.triggered.connect(lambda: self._saveSolution("brute"))
        self.ui.actionSaveEvoDAP.triggered.connect(lambda: self._saveSolution("evo_DAP"))
        self.ui.actionSaveEvoDDAP.triggered.connect(lambda: self._saveSolution("evo_DDAP"))

    def _prepareLayout(self):

        self.tabs = QtWidgets.QTabWidget(self.ui.centralwidget)

        self._prepareTables()  # add tables

        layout_general = QtWidgets.QVBoxLayout()
        layout_general.addWidget(self.tabs)

        self.ui.centralwidget.setLayout(layout_general)

    def _prepareTables(self):
        self.linkTable = QtWidgets.QTableWidget()
        self._prepareTable(self.linkTable, "Links", ["ID", "Start node", "End node", "Number of modules", "Module cost", "Link module"])

        self.demandTable = QtWidgets.QTableWidget()
        self._prepareTable(self.demandTable, "Demands", ["ID", "Start node", "End node", "Demand volume", "Number of demand paths", "Demand paths"])

        self._fillTables()

    def _prepareTable(self, table, name, col_names):
        tab_layout = QtWidgets.QVBoxLayout()
        tab = QtWidgets.QWidget()
        tab.layout = tab_layout
        self.tabs.addTab(tab, name)

        col_number = len(col_names)
        table.setColumnCount(col_number)
        table.setHorizontalHeaderLabels(col_names)
        header = table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        table.resizeRowsToContents()
        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        table.setSortingEnabled(True)

        tab.layout.addWidget(table)
        tab.setLayout(tab.layout)

    def _fillTables(self):
        for link in self.network.links:
            self._addRowToTable(self.linkTable, [link.id, link.startNode, link.endNode, link.numberOfModules,
                                                 link.moduleCost, link.linkModule])

        for demand in self.network.demands:
            row_position = self._addRowToTable(self.demandTable, [demand.id, demand.startNode, demand.endNode,
                                                                  demand.volume, demand.numberOfPaths])
            pathsString = ""
            for path in demand.paths:
                pathsString += "#" + str(path.id) + ": " + str(path.links) + "\n"
            self._insertIntoTable(self.demandTable, row_position, 5, pathsString)

    def _addRowToTable(self, table, objects):
        row_position = table.rowCount()
        table.insertRow(row_position)
        for i in range(len(objects)):
            if not (objects[i] is None):
                self._insertIntoTable(table, row_position, i, objects[i])

        return row_position

    def _insertIntoTable(self, table, row, column, obj):
        item = QtWidgets.QTableWidgetItem()
        item.setData(QtCore.Qt.DisplayRole, obj)
        table.setItem(row, column, item)

    def _insertSolutionsIntoTable(self, table, solutions, ddap):
        for solution in solutions:
            if ddap:
                objective = solution.objectiveDDAP
            else:
                objective = solution.objectiveDAP
            row_position = self._addRowToTable(table, [solution.id, objective])

            linkLoadsString = ""
            for linkLoad in solution.linkLoads:
                linkLoadsString += "#" + str(linkLoad.id) + ":  volume =" + str(linkLoad.volume) + \
                                   ", number of modules = " + str(linkLoad.numberOfModules) + "\n"
            self._insertIntoTable(table, row_position, 2, linkLoadsString)

            demandFlowsString = ""
            for demandFlow in solution.demandFlows:
                demandFlowsString += "#" + str(demandFlow.id) + ":  number of paths =" + str(
                    demandFlow.numberOfPaths) + "\n"
                demandPathsString = ""
                for pathFlow in demandFlow.pathFlows:
                    demandPathsString += "--- path #" + str(pathFlow.id) + ":  volume =" + str(pathFlow.volume) + "\n"
                demandFlowsString += demandPathsString
            self._insertIntoTable(table, row_position, 3, demandFlowsString)

    def _prepareBrute(self):
        if not (self.bruteForceSolver.bestSolutionDDAP is None):
            return

        # PROBLEM: MessageBox not updating, waits for thread?
        # msg = QtWidgets.QMessageBox()
        # msg.setIcon(QtWidgets.QMessageBox.Information)
        # msg.setText("This is a message box")
        # msg.setInformativeText("This is additional information")
        # msg.setWindowTitle("MessageBox demo")
        # msg.setDetailedText("The details are as follows:")
        # msg.show()
        # msg.update()

        self.ui.menubar.setEnabled(False)
        self.ui.centralwidget.setEnabled(False)
        self.repaint()
        self.logger.openLogFile()

        thr = Thread(target=self.bruteForceSolver.solve)
        thr.start()
        thr.join()

        file_name_DAP = "brute_force_DAP_best.txt"
        file_name_DDAP = "brute_force_DDAP_best.txt"
        serial = tools.serializer.Serializer(self.ui.errorDialog)
        serial.serializeToFile(self.network.name, file_name_DAP, self.bruteForceSolver.bestSolutionDAP)
        serial.serializeToFile(self.network.name, file_name_DDAP, self.bruteForceSolver.bestSolutionDDAP)
        self.logger.info("Best solutions saved in files:\n   output/" + self.network.name + "/" + file_name_DAP + "\n   output/" + self.network.name + "/" + file_name_DDAP)
        self.logger.closeLogFile()
        self.ui.centralwidget.setEnabled(True)
        self.ui.menubar.setEnabled(True)

        self.bruteDAPTable = QtWidgets.QTableWidget()
        self._prepareTable(self.bruteDAPTable, "Brute force DAP",
                           ["Solution ID", "Objective function (DAP)", "Link loads", "Demand flows"])
        self._insertSolutionsIntoTable(self.bruteDAPTable, self.bruteForceSolver.lastTopSolutionsDAP, ddap=False)

        self.bruteDDAPTable = QtWidgets.QTableWidget()
        self._prepareTable(self.bruteDDAPTable, "Brute force DDAP",
                           ["Solution ID", "Objective function (DDAP)", "Link loads", "Demand flows"])
        self._insertSolutionsIntoTable(self.bruteDDAPTable, self.bruteForceSolver.lastTopSolutionsDDAP, ddap=True)

    def _prepareEvolutionary(self, ddap):
        dialog = EvoInputDialog()
        if dialog.exec():
            seed, initial_population_size, number_of_offsprings, crossover_prob, mutation_prob, criterion = dialog.getInput()
        else:
            return

        self.ui.menubar.setEnabled(False)
        self.ui.centralwidget.setEnabled(False)
        self.repaint()
        self.logger.openLogFile()

        thr = Thread(target=self.evolutionarySolver.solve, kwargs={'seed': seed,
                                                                   'initial_population_size': initial_population_size,
                                                                   'ddap': ddap,
                                                                   'number_of_offsprings': number_of_offsprings,
                                                                   'crossover_prob': crossover_prob,
                                                                   'mutation_prob': mutation_prob,
                                                                   'criterion': criterion})
        thr.start()
        thr.join()

        if ddap:
            file_name = "evolutionary_DDAP_best.txt"
            solution = self.evolutionarySolver.historyOfBestChromosomesDDAP[-1]
        else:
            file_name = "evolutionary_DAP_best.txt"
            solution = self.evolutionarySolver.historyOfBestChromosomesDAP[-1]
        serial = tools.serializer.Serializer(self.ui.errorDialog)
        serial.serializeToFile(self.network.name, file_name, solution)
        self.logger.info("Best solution saved in file: output/" + self.network.name + "/" + file_name)

        self.logger.closeLogFile()
        self.ui.centralwidget.setEnabled(True)
        self.ui.menubar.setEnabled(True)

        number_of_chromosomes = 20
        if ddap:
            self.evolutionaryDDAPTable = QtWidgets.QTableWidget()
            self._prepareTable(self.evolutionaryDDAPTable, "Evolutionary DDAP",
                               ["Solution ID", "Objective function (DDAP)", "Link loads", "Demand flows"])
            to_insert = self.evolutionarySolver.historyOfBestChromosomesDDAP[-number_of_chromosomes:]
            to_insert.reverse()  # from younger to older generation (youngest was appended last)
            self._insertSolutionsIntoTable(self.evolutionaryDDAPTable, to_insert, ddap=ddap)
        else:
            self.evolutionaryDAPTable = QtWidgets.QTableWidget()
            self._prepareTable(self.evolutionaryDAPTable, "Evolutionary DAP",
                               ["Solution ID", "Objective function (DAP)", "Link loads", "Demand flows"])
            to_insert = self.evolutionarySolver.historyOfBestChromosomesDAP[-number_of_chromosomes:]
            to_insert.reverse()  # from younger to older generation (youngest was appended last)
            self._insertSolutionsIntoTable(self.evolutionaryDAPTable, to_insert, ddap=ddap)

    def _saveSolution(self, solution_type):
        if solution_type == "brute":
            if self.bruteForceSolver.bestSolutionDAP is None:
                return
            is_brute = True
            max_v = len(self.bruteForceSolver.allSolutions)
        elif solution_type == "evo_DAP":
            if len(self.evolutionarySolver.historyOfBestChromosomesDAP) == 0:
                return
            is_brute = False
            max_v = len(self.evolutionarySolver.historyOfBestChromosomesDAP)
        elif solution_type == "evo_DDAP":
            if len(self.evolutionarySolver.historyOfBestChromosomesDDAP) == 0:
                return
            is_brute = False
            max_v = len(self.evolutionarySolver.historyOfBestChromosomesDDAP)
        else:
            self.errorDialog.showMessage("ERROR (_saveSolution): Solution type unknown - \"" + solution_type + "\".")

        dialog = SaveInputDialog(brute=is_brute, max_value=max_v)
        if dialog.exec():
            chosen_solution = dialog.getInput()
        else:
            return

        if solution_type == "brute":
            if chosen_solution == "bestDAP":
                file_name = "brute_force_DAP_best.txt"
                solution = self.bruteForceSolver.bestSolutionDAP
            elif chosen_solution == "bestDDAP":
                file_name = "brute_force_DDAP_best.txt"
                solution = self.bruteForceSolver.bestSolutionDAP
            else:
                file_name = "brute_force_DAP_" + chosen_solution + ".txt"
                chosen_id = int(chosen_solution)
                solution = self.bruteForceSolver.allSolutions[chosen_id - 1]
        elif solution_type == "evo_DAP":
            if chosen_solution == "best":
                file_name = "evolutionary_DAP_best.txt"
                solution = self.evolutionarySolver.historyOfBestChromosomesDAP[-1]
            else:
                file_name = "evolutionary_DAP_" + chosen_solution + ".txt"
                chosen_id = int(chosen_solution)
                solution = self.evolutionarySolver.historyOfBestChromosomesDAP[chosen_id - 1]
        elif solution_type == "evo_DDAP":
            if chosen_solution == "best":
                file_name = "evolutionary_DDAP_best.txt"
                solution = self.evolutionarySolver.historyOfBestChromosomesDDAP[-1]
            else:
                file_name = "evolutionary_DDAP_" + chosen_solution + ".txt"
                chosen_id = int(chosen_solution)
                solution = self.evolutionarySolver.historyOfBestChromosomesDDAP[chosen_id - 1]

        serial = tools.serializer.Serializer(self.ui.errorDialog)
        serial.serializeToFile(self.network.name, file_name, solution)
        self.logger.openLogFile()
        self.logger.info("Chosen solution saved in file: output/" + self.network.name + "/" + file_name)
        self.logger.closeLogFile()


