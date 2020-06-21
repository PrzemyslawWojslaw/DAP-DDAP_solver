import os


class Serializer:
    def __init__(self, error_dialog):
        self.error_dialog = error_dialog

    def writeToFile(self, network_name, file_name, text):
        path = "output/" + network_name + "/"
        try:
            if not os.path.exists(path):
                os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        path += file_name
        try:
            textFile = open(path, 'w')
            textFile.write(text)
        except IOError:
            self.error_dialog.showMessage("Cannot create file \"" + path + "\" or write data into it.")
            return None
        else:
            textFile.close()

    def serializeToFile(self, network_name, file_name, solution):
        solution_text = self.serialize(solution)
        self.writeToFile(network_name, file_name, solution_text)

    def serialize(self, solution):
        solution_text = ""

        solution_text += str(solution.numberOfLinks) + "\n"
        for link_load in solution.linkLoads:
            link_text = str(link_load.id) + " " + str(link_load.volume) + " " + str(link_load.numberOfModules) + "\n"
            solution_text += link_text

        solution_text += "-1\n\n"

        solution_text += str(solution.numberOfDemands) + "\n\n"

        for demand_flow in solution.demandFlows:
            demand_text = str(demand_flow.id) + " " + str(demand_flow.numberOfPaths) + "\n"
            for path_flow in demand_flow.pathFlows:
                path_text = str(path_flow.id) + " " + str(path_flow.volume) + "\n"
                demand_text += path_text

            solution_text += demand_text + "\n"

        return solution_text





