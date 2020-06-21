from tools import structures
import time
import bisect
import random
import copy


class EvolutionarySolver:
    def __init__(self, error_dialog, logger, network):
        self.errorDialog = error_dialog
        self.logger = logger
        self.network = network
        self.population = None  # list of sorted Solution type objects
        self.historyOfBestChromosomesDAP = []  # list of Solution type objects
        self.historyOfBestChromosomesDDAP = []
        self.bestSolution = None  # Solution type object
        self.terminationCriterion = False

    def solve(self, seed=None, initial_population_size=10, ddap=True, number_of_offsprings=2,
              crossover_prob=0.1, mutation_prob=0.1, criterion=("time", 5)):
        # if not ddap (=False) then dap

        random.seed(seed)

        if number_of_offsprings % 2 != 0 or number_of_offsprings < 2:
            self.errorDialog.showMessage('ERROR: Number of offsprings is wrong (not even or smaller then 2).')
            return

        if crossover_prob < 0 or crossover_prob > 1 or mutation_prob < 0 or mutation_prob > 1:
            self.errorDialog.showMessage('ERROR: Wrong probability value.')
            return

        if initial_population_size < number_of_offsprings:
            self.errorDialog.showMessage('ERROR: Initial population size is too small.')
            return

        if ddap:
            self.logger.title("Evolutionary algorithm DDAP")
            type_text = "DDAP"
            self.historyOfBestChromosomes = self.historyOfBestChromosomesDDAP
        else:
            self.logger.title("Evolutionary algorithm DAP")
            type_text = "DAP"
            self.historyOfBestChromosomes = self.historyOfBestChromosomesDAP

        text = "Starting evolutionary algorithm " + type_text + " with parameters:\n"
        text += "  - Seed: " + str(seed) + "\n"
        text += "  - Initial population size: " + str(initial_population_size) + "\n"
        text += "  - Number of offsprings: " + str(number_of_offsprings) + "\n"
        text += "  - Crossover probability: " + str(crossover_prob) + "\n"
        text += "  - Mutation probability: " + str(mutation_prob) + "\n"
        text += "  - Stop criterion: "
        if criterion[0] == "time":
            text += "time (after " + str(criterion[1]) + " s)\n"
        elif criterion[0] == "number_of_generations":
            text += "number of generations (after " + str(criterion[1]) + " generations)\n"
        elif criterion[0] == "number_of_mutations":
            text += "number of mutations (after " + str(criterion[1]) + " mutations)\n"
        elif criterion[0] == "lack_of_improvement":
            text += "number of generations without improvement (after " + str(criterion[1]) + " generations)\n"
        self.logger.info(text)

        start_time = time.time()  # for time criterion

        # initialization
        self._initializePopulation(initial_population_size, ddap)
        self.historyOfBestChromosomes.clear()
        self.population[0].id = 1  # number of generation
        self.historyOfBestChromosomes.append(self.population[0])

        text = "Initialized population. Objective values (" + type_text + "):"
        for chr in self.population:
            text = text + " " + str(chr.objective)
        self.logger.info(text)

        number_of_generations = 1
        number_of_crossovers = 0
        number_of_mutations = 0
        self.terminationCriterion = False
        while not self.terminationCriterion:
            # parents selection (offsprings at the beginning are their exact copy)
            offsprings = copy.deepcopy(self.population[:number_of_offsprings])
            random.shuffle(offsprings)

            # crossover
            number_of_pairs = int(number_of_offsprings/2)
            for i in range(number_of_pairs):
                if random.random() < crossover_prob:
                    self._crossover(offsprings[i], offsprings[number_of_pairs + i])
                    number_of_crossovers += 1

            # mutation
            for offspring in offsprings:
                if random.random() < mutation_prob:
                    self._mutate(offspring)
                    number_of_mutations += 1

            # selection
            self._addToPopulation(offsprings, ddap)
            self.population = self.population[:-len(offsprings)]
            number_of_generations += 1
            best = copy.deepcopy(self.population[0])
            best.id = number_of_generations
            self.historyOfBestChromosomes.append(best)

            self._updateCriterion(criterion, start_time, number_of_generations, number_of_mutations)

        self.bestSolution = self.historyOfBestChromosomes[-1]

        elapsed_time = time.time() - start_time

        self.logger.info("SUCCESS")
        text = "Best solution objective value (" + type_text + "): " + str(self.bestSolution.objective) + "\n"
        text += "Final population objective values (" + type_text + "):"
        for chr in self.population:
            text = text + " " + str(chr.objective)
        text += "\n"
        text += "                   Time: " + str(elapsed_time) + " s\n"
        text += "  Number of generations: " + str(number_of_generations) + "\n"
        text += "   Number of crossovers: " + str(number_of_crossovers) + "\n"
        text += "    Number of mutations: " + str(number_of_mutations) + "\n"
        self.logger.info(text)


    def _initializePopulation(self, size, ddap):
        possible_demands_solutions = self._solveDemands()
        self.population = []

        for i in range(size):
            chromosome = structures.Solution(numberOfLinks=self.network.numberOfLinks,
                                             numberOfDemands=self.network.numberOfDemands)
            for possible_solutions_for_one_demand in possible_demands_solutions:
                gene = random.choice(possible_solutions_for_one_demand)
                chromosome.demandFlows.append(gene)

            chromosome.calculateLoadLinks(self.network.demands, self.network.links)
            if ddap:
                chromosome.calculateObjectiveDDAP(self.network.links)
            else:
                chromosome.calculateObjectiveDAP()
            self.population.append(chromosome)

        self.population.sort()

    def _solveDemands(self):
        """
        Create all possible flow combinations for each demand.
        IMPORTANT - link capacity not considered at this stage.

        :return: list of lists of DemandFlow objects; ID of the demand minus one is index that points to the list of its possible DemandFlows
        """
        possible_demands_solutions = []
        for demand in self.network.demands:
            # all_flows_for_demand = self._solveDemand(demand)
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

    def _crossover(self, first, second):
        for (id, demand) in enumerate(first.demandFlows):
            if random.random() < 0.5:
                temp = first.demandFlows[id]
                first.demandFlows[id] = second.demandFlows[id]
                second.demandFlows[id] = temp

    def _mutate(self, offspring):
        mutated_gene = random.choice(offspring.demandFlows)

        if mutated_gene.numberOfPaths < 2:
            return

        found = False
        while not found:  # randomly choose path with non zero demand volume
            id_giver = random.randrange(mutated_gene.numberOfPaths)
            if mutated_gene.pathFlows[id_giver].volume > 0:
                found = True

        found = False
        while not found:  # randomly choose path with non zero demand volume
            id_receiver = random.randrange(mutated_gene.numberOfPaths)
            if id_receiver != id_giver:  # find new path, different then previous
                found = True

        mutated_gene.pathFlows[id_giver].volume -= 1
        mutated_gene.pathFlows[id_receiver].volume += 1

    def _addToPopulation(self, offsprings, ddap):
        for offspring in offsprings:
            offspring.calculateLoadLinks(self.network.demands, self.network.links)
            if ddap:
                offspring.calculateObjectiveDDAP(self.network.links)
            else:
                offspring.calculateObjectiveDAP()

            bisect.insort(self.population, offspring)

    def _updateCriterion(self, criterion, start_time, number_of_generations, number_of_mutations):
        criterion_type, criterion_value = criterion

        if criterion_type == "time":
            if time.time() - start_time > criterion_value:
                self.terminationCriterion = True
        elif criterion_type == "number_of_generations":
            if number_of_generations >= criterion_value:
                self.terminationCriterion = True
        elif criterion_type == "number_of_mutations":
            if number_of_mutations >= criterion_value:
                self.terminationCriterion = True
        elif criterion_type == "lack_of_improvement":
            if number_of_generations < criterion_value:
                return
            improvement = False
            check_list = self.historyOfBestChromosomes[-criterion_value:]
            for (id, chromosome) in enumerate(check_list[:-1]):

                if check_list[id] > check_list[id+1]:
                    improvement = True
                    break

            if not improvement:
                self.terminationCriterion = True
