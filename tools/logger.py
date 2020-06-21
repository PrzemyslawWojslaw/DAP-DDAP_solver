import datetime
import os


class Logger:
    def __init__(self, network_name):
        self.logFile = None
        self.path = "output/" + network_name + "/"
        try:
            if not os.path.exists(self.path):
                os.mkdir(self.path)
        except OSError:
            print("Creation of the directory %s failed" % self.path)

        current_time = datetime.datetime.now()
        current_date = current_time.strftime("%Y-%m-%d")
        self.path += "logs_" + current_date + ".txt"

    def openLogFile(self):
        current_time = datetime.datetime.now()
        current_date = current_time.strftime("%Y-%m-%d")
        try:
            self.logFile = open(self.path, 'a')
            self.logFile.write("\n==============================\n")
            print("\n==============================\n")
            self.logFile.write("   " + current_date + "\n")
        except IOError:
            print("LOGGER: Cannot create file \"" + self.path + "\" or write data into it!")

    def closeLogFile(self):
        self.logFile.write("\n==============================\n")
        print("\n==============================\n")
        self.logFile.close()

    def title(self, text):
        text = "   " + text
        print(text)
        if (self.logFile is not None) and (not self.logFile.closed):
            self.logFile.write(text + "\n")

    def info(self, text):
        current_time = datetime.datetime.now()
        text = current_time.strftime("[%H:%M:%S] INFO >> ") + text
        print(text)
        if (self.logFile is not None) and (not self.logFile.closed):
            self.logFile.write(text + "\n")

    def error(self, text):
        current_time = datetime.datetime.now()
        text = current_time.strftime("[%H:%M:%S] ERROR >> ") + text
        print(text)
        if (self.logFile is not None) and (not self.logFile.closed):
            self.logFile.write(text + "\n")
