from tools import structures


class Parser:
    def __init__(self, error_dialog):
        self.errorDialog = error_dialog

    def parseFile(self, path):
        try:
            textFile = open(path, 'r')
            networkText = textFile.read()
        except IOError:
            self.errorDialog.showMessage("Cannot find file \"" + path + "\" or read data from it.")
            return None
        else:
            textFile.close()
            full_name = path.split('/')[-1]
            name = full_name.split('.')[0]
            network = self.parse(name, networkText)

        return network

    def parse(self, name, text):
        lines = text.splitlines()
        net = structures.Network(name)

        net.numberOfLinks = int(lines[0])
        if lines[net.numberOfLinks+1] != "-1":
            self.errorDialog.showMessage("ERROR: Number of links or position of \"-1\" separator is wrong.")
            return None

        linkLines = lines[1:net.numberOfLinks + 1]
        net.links = self._parseLinkLines(linkLines)

        if net.numberOfLinks != len(net.links):
            self.errorDialog.showMessage("ERROR: Found " + str(len(net.links)) + " of links, but declared " + str(net.numberOfLinks) + ".")
            return None

        net.numberOfDemands = int(lines[net.numberOfLinks+3])
        demandLines = lines[net.numberOfLinks+4:]
        net.demands = self._parseDemandLines(demandLines)

        if net.numberOfDemands != len(net.demands):
            self.errorDialog.showMessage("ERROR: Found " + str(len(net.demands)) + " of demands, but declared " + str(net.numberOfDemands) + ".")
            return None

        return net

    def _parseLinkLines(self, linkLines):
        links = []
        currentId = 0

        for line in linkLines:
            values = line.split(" ")
            currentId += 1  # IDs should start with 1
            newLink = structures.Link(id=currentId,
                                      startNode=int(values[0]),
                                      endNode=int(values[1]),
                                      numberOfModules=int(values[2]),
                                      moduleCost=int(values[3]),
                                      linkModule=int(values[4]))
            links.append(newLink)

        return links

    def _parseDemandLines(self, demandLines, currentId=1):
        demands = []

        # end of recursion when found additional empty line (len == 1) or no additional lines (len == 0) at the end of file
        if len(demandLines) == 0 or (len(demandLines) == 1 and demandLines[0] == ""):
            return demands

        if demandLines[0] != "":
            self.errorDialog.showMessage("ERROR: During parsing of demand #" + str(currentId) + " emcountered \"" + demandLines[0] + "\" instead of expected empty line.")
            return None

        if len(demandLines) < 2:
            self.errorDialog.showMessage("ERROR: Wrong number of lines in declaration of demand #" + str(currentId) + ".")
            return demands

        mainDemandLine = demandLines[1]
        numberOfPaths = int(demandLines[2])

        if len(demandLines) < 2 + numberOfPaths:
            self.errorDialog.showMessage("ERROR: Wrong number of lines in declaration of demand #" + str(currentId) + ".")
            return demands

        values = mainDemandLine.split(" ")
        newDemand = structures.Demand(id=currentId,
                                      startNode=int(values[0]),
                                      endNode=int(values[1]),
                                      volume=int(values[2]),
                                      numberOfPaths=numberOfPaths)
        demandPathsLines = demandLines[3:3 + numberOfPaths]
        demandPaths = self._parseDemandPaths(demandPathsLines)
        newDemand.paths = demandPaths
        demands.append(newDemand)

        demands += self._parseDemandLines(demandLines[3 + numberOfPaths:], currentId + 1)   # recursively read next demands

        return demands

    def _parseDemandPaths(self, demandPathLines):
        demandPaths = []

        for line in demandPathLines:
            values = line.split(" ")
            values[:] = (val for val in values if val != "")  # removal of values "between" double spaces
            idList = [int(i) for i in values[1:]]
            path = structures.DemandPath(id=values[0], linkIdList=idList)
            demandPaths.append(path)
        return demandPaths
