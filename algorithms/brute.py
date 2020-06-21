from tools import structures
import itertools
import time


class BruteForceSolver:
    def __init__(self, error_dialog, logger, network, max_top_solutions=30):
        self.errorDialog = error_dialog
        self.logger = logger
        self.network = network
        self.allSolutions = []  # list of Solution type objects
        self.maxTopSolutions = max_top_solutions  # how many solutions to remember
        self.lastTopSolutionsDAP = []  # lists of top solutions
        self.lastTopSolutionsDDAP = []
        self.bestSolutionDAP = None  # Solution type object
        self.bestSolutionDDAP = None  # Solution type object

    def solve(self):
        self.logger.title("Brute force algorithm for DAP and DDAP")
        self.logger.info("Starting brute force solving. It may take a while...")

        start_time = time.time()

        possible_demands_solutions = self._solveDemands()
        self._prepareSolutions(possible_demands_solutions)

        elapsed_time = time.time() - start_time

        self.logger.info("SUCCESS")
        text = "Best solutions: \n"
        text += "     a) DAP - ID:" + str(self.bestSolutionDAP.id) + ", objecive value: " + str(self.bestSolutionDAP.objectiveDAP) + "\n"
        text += "     a) DDAP - ID:" + str(self.bestSolutionDDAP.id) + ", objecive value: " + str(self.bestSolutionDDAP.objectiveDDAP) + "\n"
        text += "\n"
        text += "                   Time: " + str(elapsed_time) + " s\n"
        text += "    Number of solutions: " + str(len(self.allSolutions)) + "\n"
        self.logger.info(text)

    def _solveDemands(self):
        """
        Create all possible flow combinations for each demand.
        IMPORTANT - link capacity not considered at this stage.

        :return: list of lists of DemandFlow objects; ID of the demand minus one is index that points to the list of its possible DemandFlows
        """
        possible_demands_solutions = []
        for demand in self.network.demands:
            all_flows_for_demand = self._recFindFlows(demand.id, 1, demand.numberOfPaths, demand.volume)
            for demand_flow in all_flows_for_demand:
                demand_flow.pathFlows.reverse()  # flows were appended starting form the last

            possible_demands_solutions.append(all_flows_for_demand)

        return possible_demands_solutions

    def _recFindFlows(self, curd, curp, maxp, lefth):
        """
        Recursively find all possible DemandFlows for given demand.
        IMPORTANT - link capacity not considered at this stage.

        :param curd: ID of the current demand
        :param curp: ID of the current path
        :param maxp: number of paths in current demand
        :param lefth: demand volume left to distribute
        :return: list of DemandFlow objects
        """
        list_of_possible_combinations = []  # list of DemandFlow objects

        if curp == maxp:
            demand_flow = structures.DemandFlow(curd, maxp)
            path_flow = structures.DemandPathFlow(curp, lefth)
            demand_flow.pathFlows.append(path_flow)
            list_of_possible_combinations.append(demand_flow)
        else:
            for parth in range(lefth+1):

                short_list_possible_combinations = self._recFindFlows(curd, curp + 1, maxp, lefth - parth)
                for demand_flow in short_list_possible_combinations:
                    path_flow = structures.DemandPathFlow(curp, parth)
                    demand_flow.pathFlows.append(path_flow)

                list_of_possible_combinations += short_list_possible_combinations

        return list_of_possible_combinations

    def _prepareSolutions(self, possible_demands_solutions):
        solution_id = 0
        for combinations_of_demands_flows in itertools.product(*possible_demands_solutions):
            solution_id += 1
            solution = structures.Solution(solutionId=solution_id,
                                           numberOfLinks=self.network.numberOfLinks,
                                           numberOfDemands=self.network.numberOfDemands)
            solution.demandFlows = list(combinations_of_demands_flows)
            solution.calculateLoadLinks(self.network.demands, self.network.links)

            solution.calculateObjectiveDAP()
            if len(self.lastTopSolutionsDAP) < self.maxTopSolutions or solution.objectiveDAP < self.lastTopSolutionsDAP[-1].objectiveDAP:
                self.lastTopSolutionsDAP.append(solution)
                self.lastTopSolutionsDAP.sort(key=lambda x: x.objectiveDAP)
                if len(self.lastTopSolutionsDAP) > self.maxTopSolutions:
                    self.lastTopSolutionsDAP.pop()

            # reminder - calculation of obejctive changes self.objective for comparision (insort)
            solution.calculateObjectiveDDAP(self.network.links)
            if len(self.lastTopSolutionsDDAP) < self.maxTopSolutions or solution.objectiveDDAP < self.lastTopSolutionsDDAP[-1].objectiveDDAP:
                self.lastTopSolutionsDDAP.append(solution)
                self.lastTopSolutionsDDAP.sort(key=lambda x: x.objectiveDDAP)
                if len(self.lastTopSolutionsDDAP) > self.maxTopSolutions:
                    self.lastTopSolutionsDDAP.pop()

            self.allSolutions.append(solution)
        self.bestSolutionDAP = self.lastTopSolutionsDAP[0]
        self.bestSolutionDDAP = self.lastTopSolutionsDDAP[0]
