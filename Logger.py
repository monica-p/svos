from time import gmtime,strftime

class Logger(object):
    """

    Class keeps log of every program Run
    """
    logFile = None

    @classmethod
    def initialize(cls):
        inputFile = 'logFile.txt'
        mode = 'a+'

        Logger.logFile = open(inputFile,mode)

    @classmethod
    def enterLog(cls,entry):
        time = strftime('%d/%m/%Y %H:%M:%S' , gmtime())
        Logger.logFile.write(time + '-->' + entry + '\n')
        Logger.logFile.flush()

