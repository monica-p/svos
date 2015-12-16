from SystemQueue import SystemQueue
from PCB import PCB
from Printer import Printer
from Memory import Memory
from globalFuncions import *
from Logger import Logger

inputFile = 'Tempinput.txt'
mode = 'r'

progFile = open(inputFile,mode)
 
class Channel(object):
    """description of class"""
   
    def __init__(self):
       self.channel1 = Channel.inputSpooling()
       self.channel2 = Channel.outputSpooling()
       self.channel3 = Channel.loading()

       self.channelList = [self.channel1,self.channel2,self.channel3]


        
    def incChannelTimer(self,busyList):
        for channel in busyList:
            channel.incTimer()

    def ChannelIdle(self):
        count = 0
        for ch in self.channelList:
            if ch.ChannelBusy == False:
                count += 1
        if count == 3:
            return True
        else:
            return False

    class inputSpooling(object):

        def __init__(self):
            self.ChannelName = 'channel1'
            self.timer = 0
            self.busy = False
            self.totalTime = 5

            self.NextCardflag = str()
            self.emptybuffer = None
            self.ipbuffer = None

            self.progPCB = None
           
        def incTimer(self):
            self.timer = self.timer + 1
        
        @property    
        def ChannelBusy(self):
            return self.busy

        @ChannelBusy.setter
        def ChannelBusy(self,Value):
            self.busy = Value

        
        def run(self):
            if not self.emptybuffer == None:
                self.emptybuffer.Type = "IP"
                self.ipbuffer = self.emptybuffer

            if not SystemQueue.EmptyBufferQueue.empty():
                self.emptybuffer = SystemQueue.EmptyBufferQueue.get()
            
            if not self.ipbuffer == None and self.ipbuffer.Type == "IP":
                line = progFile.readline()

                if "$AMJ" in line:
                    self.progPCB = PCB()
                    self.progPCB.PTR = Memory.UserStorage.AllocatePage()

                    PCBdata = line.split(" ")
                    self.progPCB.PID = PCBdata[1]
                    self.progPCB.TLL = PCBdata[2]
                    self.progPCB.TTL = PCBdata[3]


                    self.NextCardflag = "PROG"
                    self.ipbuffer.Type = "Empty"
                    SystemQueue.EmptyBufferQueue.put(self.ipbuffer)
                
                elif "$DTA" in line:
                    self.NextCardflag = "DATA"
                    self.ipbuffer.Type = "Empty"
                    SystemQueue.EmptyBufferQueue.put(self.ipbuffer)
                
                elif "$END" in line:
                    
                    self.progPCB.programCard = self.progPCB.ProgCardCounter
                    self.progPCB.DataCard = self.progPCB.DataCardCounter

                    SystemQueue.LoadQueue.put(self.progPCB)
                    self.progPCB = None
                    SystemQueue.EmptyBufferQueue.put(self.emptybuffer)

                elif line == '': 
                    self.busy = False
                    
                else:
                    wordList = MakeWord(filterList(list(line)))
                    card = MakeCard(wordList)
                    self.ipbuffer.LoadBuffer(card)
                    self.ipbuffer.Type = "IP"

                    if self.NextCardflag == "PROG":
                        self.progPCB.ProgCardCounter += 1
                    elif self.NextCardflag == "DATA":
                        self.progPCB.DataCardCounter += 1

                    SystemQueue.InputBufferQueue.put(self.ipbuffer)
                    SystemQueue.EmptyBufferQueue.put(self.emptybuffer)


              

    class outputSpooling(object):
        
        def __init__(self):
            self.ChannelName = 'channel2'
            self.timer = 0
            self.busy = False
            self.totalTime = 5
            self.outputBuffer = None

        def incTimer(self):
            self.timer = self.timer + 1
            
        @property    
        def ChannelBusy(self):
            return self.busy

        @ChannelBusy.setter
        def ChannelBusy(self,Value):
            self.busy = Value

        def run(self):
            data = ""
            if not self.outputBuffer == None:
                if self.outputBuffer.Type == "OP":
                    data = ReadCard(self.outputBuffer.UnloadBuffer())
                    Printer.enterLog("Data: " +  data)
                    self.outputBuffer.Type = "Empty"
                    SystemQueue.EmptyBufferQueue.put(self.outputBuffer)

            if not SystemQueue.OutBufferQueue.empty():
                self.outputBuffer = SystemQueue.OutBufferQueue.get()
                size = SystemQueue.OutBufferQueue.qsize()
                
                

    class loading(object):
        
        def __init__(self):
            self.ChannelName = 'channel3'
            self.timer = 0
            self.busy = False
            self.totalTime = 3

            self.task = None

            self.ipBuffer = None
            self.opBuffer = None
            
            self.currISPCB = None
            self.currOSPCB = None
            self.currLoadPCB = None
            self.currReadPCB = None
            self.currWritePCB = None
            self.currEndPCB = None

            self.ISTrack = int()
            self.OSTrack = int()
            self.LoadTrack = int()

            self.opTrackCard = list(list())
            self.opTrackNo = int()

            self.IOReadTrack = int()
            self.IOWriteTrack = int()

            self.loadFlag = False

            self.MemoryBlock = int()

            self.indicatedMemory = int()

            self.opBuffer = None
            self.opCounter = int()
            self.auxilaryPrintCount = int()
        
        def incTimer(self):
            self.timer = self.timer + 1 

        @property    
        def ChannelBusy(self):
            return self.busy

        @ChannelBusy.setter
        def ChannelBusy(self,Value):
            self.busy = Value

        def run(self):
            if not self.task == None:
                if self.task == "IS" and self.currISPCB != None:
                    if self.ipBuffer.Type == "IP":
                        Memory.AuxillaryStorage.Drum[self.ISTrack] = self.ipBuffer.UnloadBuffer()

                        if self.currISPCB.ProgCardCounter != 0:
                             self.currISPCB.ProgCardCounter -= 1
                             self.currISPCB.updateDrumPageTable("P",self.ISTrack)
                        elif self.currISPCB.DataCardCounter != 0:
                             self.currISPCB.DataCardCounter -= 1
                             self.currISPCB.updateDrumPageTable("D",self.ISTrack)

                      
                        if self.currISPCB.ProgCardCounter == 0 and self.loadFlag == False:
                            SystemQueue.USLoadQueue.put(self.currISPCB)
                            self.loadFlag = True
                        if self.currISPCB.DataCardCounter == 0:
                            self.currISPCB = None

                elif self.task == "LD":
                    #loading tabhi chalu karo jab sare prog card drum me a gaye ho!
                    if not self.LoadTrack == None: 
                        if not self.currLoadPCB.ProgCardCounter == self.currLoadPCB.TPC:
                            self.currLoadPCB.ProgCardCounter += 1

                            #location = Memory.UserStorage.GetMemoryLocation()
                            Memory.UserStorage.LoadMemory(self.LoadTrack,self.MemoryBlock)
                            self.LoadTrack = None

                            if self.currLoadPCB.ProgCardCounter == self.currLoadPCB.TPC:
                                loadPCB = self.currLoadPCB
                                SystemQueue.ReadyQueue.put(loadPCB)
                                size = SystemQueue.ReadyQueue.qsize()
                                self.currLoadPCB = None

                elif self.task == "RD":
                    if not self.IOReadTrack == None:
                        if not self.currReadPCB.DataCardCounter == self.currReadPCB.DataCard:
                            self.currReadPCB.DataCardCounter += 1

                            Memory.UserStorage.LoadMemory(self.IOReadTrack,self.currReadPCB.IOReadLoc/10)
                            readyPcb = self.currReadPCB
                            readyPcb.TSC = 0
                            
                            if not self.currReadPCB.terminated:
                                SystemQueue.ReadyQueue.put(readyPcb)
                                size = SystemQueue.ReadyQueue.qsize()
                            self.IOReadTrack = None

                            if self.currReadPCB.DataCardCounter == self.currReadPCB.DataCard:
                                self.currReadPCB = None

                elif self.task == "WT":
                    if not self.IOWriteTrack == None:
                        Memory.AuxillaryStorage.Drum[self.OSTrack] = self.IOWriteTrack
                        

                        opReadyPcb = self.currOSPCB
                        opReadyPcb.TSC = 0

                        if not self.currOSPCB.terminated:
                            SystemQueue.ReadyQueue.put(opReadyPcb)
                            size = SystemQueue.ReadyQueue.qsize()

                        if self.auxilaryPrintCount == self.currOSPCB.OPCounter:
                            self.currOSPCB = None
                            self.auxilaryPrintCount = 0

                        self.IOWriteTrack = None

                elif self.task == "OS":
                    if not self.opTrackCard == None:
                        if self.opBuffer.Type == "OP":
                            self.opBuffer.LoadBuffer(self.opTrackCard)
                            SystemQueue.OutBufferQueue.put(self.opBuffer)
                            #Memory.AuxillaryStorage.clearTrack(self.opTrackNo)
                        
                            if self.opCounter == len(self.currEndPCB.drumPagetable["OP"]):
                                self.opCounter = 0
                                self.currEndPCB = None
                                self.opTrackCard = None

                elif self.task == "END":
                    #for en in self.currEndPCB.pageFrameNo:
                    #    Memory.UserStorage.clearArray(en)

                    #for enTP in self.currEndPCB.drumPagetable["P"]:
                    #    Memory.AuxillaryStorage.clearTrack(enTP)

                    #for enTD in self.currEndPCB.drumPagetable["D"]:
                    #    Memory.AuxillaryStorage.clearTrack(enTD)
                    self.currEndPCB = None


            if not SystemQueue.TerminateQueue.empty() or self.currEndPCB != None:

                if self.currEndPCB == None:
                     self.currEndPCB = SystemQueue.TerminateQueue.get()

                if len(self.currEndPCB.drumPagetable["OP"]) == 0:
                    self.task = "END"

                else:

                    if not SystemQueue.EmptyBufferQueue.empty():
                        self.opBuffer = SystemQueue.EmptyBufferQueue.get()
                        self.opBuffer.Type = "OP"

                    self.opTrackNo = self.currEndPCB.drumPagetable["OP"][self.opCounter]
                    self.opTrackCard = Memory.AuxillaryStorage.Drum[self.opTrackNo]
                    self.opCounter += 1
                    self.task = "OS"

                

                    #for en in self.currEndPCB.pageFrameNo:
                    #    Memory.UserStorage.clearArray(en)

                    #for enTP in self.currEndPCB.drumPagetable["P"]:
                    #    Memory.AuxillaryStorage.clearTrack(enTP)

                    #for enTD in self.currEndPCB.drumPagetable["D"]:
                    #    Memory.AuxillaryStorage.clearTrack(enTD)

                #for enOP in self.currEndPCB.drumPagetable["D"]:
                #    Memory.AuxillaryStorage.clearTrack(enOP)
           
            elif not SystemQueue.LoadQueue.empty() or self.currISPCB != None:
                if self.currISPCB == None or self.currISPCB.DataCardCounter == 0:
                    self.currISPCB = SystemQueue.LoadQueue.get()
                    self.loadFlag = False
                if not SystemQueue.InputBufferQueue.empty():
                    self.ipBuffer = SystemQueue.InputBufferQueue.get()
                    self.ipBuffer.BufferShow()
                    self.ISTrack = Memory.AuxillaryStorage.GetTrack()
                    self.task = "IS"
                    #start channel 3

            elif not SystemQueue.USLoadQueue.empty() or self.currLoadPCB != None:
                if self.currLoadPCB == None or self.currLoadPCB.ProgCardCounter == self.currLoadPCB.programCard:
                    self.currLoadPCB = SystemQueue.USLoadQueue.get()
                else:
                    if self.currLoadPCB.PTR == None:
                        self.currLoadPCB.PTR = Memory.UserStorage.AllocatePage()
                        self.currLoadPCB.pageFrameNo.append(self.currLoadPCB.PTR)

                    trackNo = self.currLoadPCB.returnTrackNo("P",self.currLoadPCB.ProgCardCounter)
                    self.LoadTrack = Memory.AuxillaryStorage.Drum[trackNo]

                    self.MemoryBlock = Memory.UserStorage.AllocatePage()
                    self.currLoadPCB.pageFrameNo.append(self.MemoryBlock)
                    Memory.UserStorage.updateTable(self.MemoryBlock,self.currLoadPCB.pageTablePointer,self.currLoadPCB)
                    self.currLoadPCB.pageTablePointer += 10
                    self.task = "LD"

                    for i in range(0,300):
                        if len(Memory.UserStorage.MemoryList[i]) > 0:
                            print str(i) + ":" + str(Memory.UserStorage.MemoryList[i])

            elif not SystemQueue.IOReadQueue.empty() or self.currReadPCB != None:
                if self.currReadPCB == None or self.currReadPCB.DataCardCounter == self.currReadPCB.DataCard:
                    self.currReadPCB = SystemQueue.IOReadQueue.get()

                else:
                    DtrackNo = self.currReadPCB.returnTrackNo("D",self.currReadPCB.DataCardCounter)
                    self.IOReadTrack = Memory.AuxillaryStorage.Drum[DtrackNo]
                    self.task = "RD"

            elif not SystemQueue.IOWriteQueue.empty() or self.currOSPCB != None:

                if self.currOSPCB == None:
                    self.currOSPCB = SystemQueue.IOWriteQueue.get()

                if self.currOSPCB.TLC > self.currOSPCB.TLL:
                    SystemQueue.TerminateQueue.put(currOSPCB)
                    Logger.enterLog('Process- ' + str(self.currOSPCB.PID) + ': Line Limit Exceeded')
                else:
                    self.OSTrack = Memory.AuxillaryStorage.GetTrack()
                    self.currOSPCB.updateDrumPageTable("OP",self.OSTrack)
                    self.IOWriteTrack = Memory.UserStorage.ReadMemory(self.currOSPCB.IOWriteLoc)
                    self.auxilaryPrintCount += 1
                    self.task = "WT"



              

