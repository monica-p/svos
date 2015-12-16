class PCB(object):
    """description of class"""


    def __init__(self):
        
        #Processing related parameters
        self.TLL = int()
        self.TTL = int()
        self.PTR = None
        self.PID = int()
        self.IC = ["0","0"]
        self.TTC = 0
        self.TLC = 0
        self.timeSlice = 5
        self.TSC = 0

        #Scheduling related parameters
        self.arrivalTime = int()
        self.serviceTime = int()
        self.finishTime = int()
        self.executionTime = int()
        self.waitingTime = int()
        self.turnAroundTime = int()

        #memory management related parameters
        self.ProcessPageTable = list(list())
        self.pageTablePointer = int()

        #Spooling Management
        self.drumPagetable = {"P":[],"D":[],"OP":[]}

        self.ProgCardCounter = 0
        self.DataCardCounter = 0
        self.OPCounter = 0

        self.TPC = int()
        self.TDC = int()

        self.pageFrameNo = []

        #IO Management
        self.IOReadLoc = int()
        self.IOWriteLoc = int()

        #Termination
        self.terminated = False

    @property
    def programCard(self):
        return self.TPC
    
    @programCard.setter
    def programCard(self,value):
        self.TPC = value

    @property
    def DataCard(self):
        return self.TDC
    
    @DataCard.setter
    def DataCard(self,value):
        self.TDC = value

    def updateDrumPageTable(self,cardType,TrackNo):
        self.drumPagetable[cardType].append(TrackNo)

    def returnTrackNo(self,cardType,CardNo):
        return self.drumPagetable[cardType][CardNo]


