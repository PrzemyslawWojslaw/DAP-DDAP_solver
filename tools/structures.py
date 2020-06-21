import math


# if type not specified, then integer

##########################
###  NETWORK objects  ###
##########################

class Network:
    def __init__(self, name):
        self.name = name  # network file name (without .txt)
        self.numberOfLinks = 0  # always equal to len(self.links)
        self.links = []  # list of Link objects
        self.numberOfDemands = 0  # always equal to len(self.numberOfDemands)
        self.demands = []  # list of Demand objects


class Link:
    def __init__(self, id, startNode, endNode, numberOfModules, moduleCost, linkModule):
        self.id = id
        self.startNode = startNode
        self.endNode = endNode
        self.numberOfModules = numberOfModules  # max number of fibre modules in cable
        self.moduleCost = moduleCost
        self.linkModule = linkModule  # number of fibres in module
        # link capacity = numberOfModules * linkModule


class Demand:
    def __init__(self, id, startNode, endNode, volume, numberOfPaths):
        self.id = id
        self.startNode = startNode
        self.endNode = endNode
        self.volume = volume
        self.numberOfPaths = numberOfPaths
        self.paths = []  # list of DemandPath objects

class DemandPath:
    def __init__(self, id, linkIdList):
        self.id = id
        self.links = linkIdList  # list of integers

##########################
###  SOLUTION objects  ###
##########################

# changed "signal" nomenclature to "volume" one

class Solution:
    def __init__(self, solutionId=0, numberOfLinks=0, numberOfDemands=0):
        self.id = solutionId
        self.numberOfLinks = numberOfLinks  # at the end should be equal to len(self.linkLoads)
        self.linkLoads = []  # list of LinkLoad objects
        self.numberOfDemands = numberOfDemands  # at the end should be equal to len(self.demandFlows)
        self.demandFlows = []  # list of DemandFlow objects

        self.objectiveDAP = None  # for brute force, allows to solve both DAP and DDAP in the same time
        self.objectiveDDAP = None  # as above
        self.objective = None  # for comparing in evolutionary algorithm, equal to objectiveDAP or objectiveDDAP (depending which one was calculated last)

    def __eq__(self, other):
        return self.objective == other.objective

    def __lt__(self, other):
        return self.objective < other.objective

    def __gt__(self, other):
        return self.objective > other.objective

    def calculateLoadLinks(self, demands, links):  # parameter "demands" is list from Network.demands, "links" - Network.links
        self.linkLoads.clear()

        for load_id in range(self.numberOfLinks):
            link_load = LinkLoad(load_id + 1, 0, 0)
            self.linkLoads.append(link_load)

        for (demand_id, demand_flow) in enumerate(self.demandFlows):
            for (path_id, path_flow) in enumerate(demand_flow.pathFlows):
                for link_id in demands[demand_id].paths[path_id].links:
                    self.linkLoads[link_id - 1].volume += path_flow.volume  # link_id there starts from 1

        for (link_id, link_load) in enumerate(self.linkLoads):  # link_id there starts from 0
            link_load.numberOfModules = math.ceil(link_load.volume / links[link_id].linkModule)
            if link_load.numberOfModules > links[link_id].numberOfModules:
                pass  # TODO: remove this solution from list, it's not feasible

    def calculateObjectiveDAP(self):  # parameter "links" is list from Network.links
        objective_value = 0
        for (link_id, link_load) in enumerate(self.linkLoads):
            # link_capacity = links[link_id].numberOfModules * links[link_id].linkModule
            # obj = link_load.volume - link_capacity
            obj = link_load.volume
            if obj > objective_value:
                objective_value = obj
        self.objectiveDAP = objective_value
        self.objective = objective_value
        return self.objectiveDAP

    def calculateObjectiveDDAP(self, links):  # parameter "links" is list from Network.links
        objective_value = 0
        for (link_id, link_load) in enumerate(self.linkLoads):
            link_cost = link_load.numberOfModules * links[link_id].moduleCost
            objective_value += link_cost
        self.objectiveDDAP = objective_value
        self.objective = objective_value
        return self.objectiveDDAP


class LinkLoad:
    def __init__(self, id, volume, numberOfModules):
        self.id = id
        self.volume = volume  # previously: numberOfSignals
        self.numberOfModules = numberOfModules  # number of fiber modules used to deliver load

class DemandFlow:
    def __init__(self, id, numberOfPaths):
        self.id = id  # ID of demand
        self.numberOfPaths = numberOfPaths
        self.pathFlows = []  # list of DemandPathFlow objects

class DemandPathFlow:
    def __init__(self, id, volume):
        self.id = id  # ID of path belonging to considered demand
        self.volume = volume  # previously: signalsCount

