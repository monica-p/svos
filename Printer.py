from time import gmtime,strftime

class Printer(object):
    """

    Class keeps log of every program Run
    """
    opFile = None

    @classmethod
    def initialize(cls):
        OutPutFile = 'output.txt'
        mode = 'a+'

        Printer.opFile = open(OutPutFile,mode)

    @classmethod
    def enterLog(cls,entry):
        time = strftime('%d/%m/%Y %H:%M:%S' , gmtime())
        Printer.opFile.write(time + '-->' + entry + '\n')
        Printer.opFile.flush()
