'''
IOI ko decrease ni kia kahi avi tak


'''
from Memory import Memory
from Logger import Logger
import re
from SystemQueue import SystemQueue
from globalHelp import channel
#from globalFuncions import PutData
from globalFuncions import roundOff
#import Memory.Memory as Memory

class CPU(object):
    """description of class"""

    

    def __init__(self):
        '''
        constructor definition
        '''
        self.Register = list()      	#--> Can contain only 4 characters (4bytes)
        self.IC = [0,0]            	    #--> conatins index of memory location to be read (contains only two charc)
        self.boolFlag = bool()          	#--> Set or reset in compare operations etc
        self.IR = list()            	#--> Can contain only 4 characters (4bytes) (2 bytes opcode, 2bytes operand)
        self.programCounter = int()
        self.interruptvalidator = int() #--> Validates if $DTA is present at first call of read interrupt
        self.halt = int()		        #--> terminates the current program
        self.terminator = int()

        self.currentProgram = None
        self.PI = int()                 #--> Interrupt   1. Operation Error
                                        #       2. Operand Error
                                        #       3. Page Fault 
        self.TI = int()                 #--> Interrupt 2. Time limit exceeded.
        self.SI = int()                 #--> Interrupt 1.Write to Memory Read from input
                                            #     2.Read from Memory Write to output
                                            #     3. Halt

        self.IOI = 0

        self.readInst = ['lr','cr','pd','inst']
        self.writeInst = ['sr','gd']
        


    def incIC(self):
        '''
        increaments the instruction counter after execution of every instruction
        '''
        ICstr = self.IC[0] + self.IC[1]
        ICvalue = int(ICstr) + 1
        self.IC[0] = str(ICvalue//10)
        self.IC[1] = str(ICvalue % 10)

    def decIC(self):
        '''
        increaments the instruction counter after execution of every instruction
        '''
        ICstr = self.IC[0] + self.IC[1]
        ICvalue = int(ICstr) - 1
        self.IC[0] = str(ICvalue//10)
        self.IC[1] = str(ICvalue % 10)

    def resetIC(self):
        '''
        resets Instruction counter to zero
        '''
        self.IC[0] = '0'
        self.IC[1] = '0'

    @property
    def ICValue(self):
        '''
        '''
        IC = self.IC[0] + self.IC[1]
        return IC

    @ICValue.setter
    def ICValue(self,value):
        '''
        '''
        self.IC[0] = str(value//10)
        self.IC[1] = str(value % 10)

    @property
    def Flag(self):
        '''
        Returns boolean flag of register C
        '''
        return self.boolFlag

    @Flag.setter
    def Flag(self,value):
        '''
        Sets boolean flag of register C
        '''
        self.boolFlag = value

    @property
    def Terminate(self):
        return self.terminator

    @Terminate.setter
    def Terminate(self,value):
        self.terminator = value

    @property
    def PC(self):
        return self.programCounter
    
    @PC.setter
    def PC(self,value):
        self.programCounter = value

    @property
    def IRValue(self):
        '''
        sets instruction register with appropriate instruction
        '''
        return self.IR

    @IRValue.setter
    def IRValue(self,value):
        '''
        sets instruction register with appropriate instruction
        '''
        self.IR = value

    def LoadToRegister(self,RA):
        '''
        Takes data from passed Memory location and load it to register.
        para: MemoryLocation
        1.mapp address
        2.Load to CPU register
        remark:
            1. Takes one word at a time for register is only 4bytes.
        '''
        #RA = Memory.MapAddress(address)
        self.Register = Memory.UserStorage.MemoryList[RA]

    def StoreFromRegister(self,RA):
        '''
        Takes data from register and store it at memory location passed in memory.
        
        1.mapp address
        2.Load Store CPU register to Memory
        
        para: MemoryLocation
        '''
        #RA = Memory.MapAddress(address)
        Memory.UserStorage.MemoryList[RA] = self.Register

    def Halt(self,ProgFile):
        '''
        '''
        self.halt = 1
        haltTest = ''
        while(not "END" in haltTest):
            haltTest = ProgFile.readline()
        print "Program Ended"

    def CompareReg(self,address):
        '''
        '''
        if self.Register == Memory.UserStorage.MemoryList[address]:
            self.Flag = True
        else:
            self.Flag = False

    def execute(self,instruction,address):
        '''
        1.Takes in instruction
        2.Performs task accordingly
        3.Set PI 3 operation error occurs

        '''
        pattern = {'LR':r'[Ll][Rr]','SR':r'[Ss][Rr]','CR':r'[Cc][Rr]','BT':r'[Bb][Tt]','GD':r'[Gg][Dd]','PD':r'[Pp][Dd]','H':r'[Hh]'}

        if (re.match(pattern['LR'],instruction)):
            self.LoadToRegister(address)
        elif (re.match(pattern['SR'],instruction)):
            self.StoreFromRegister(address)
        elif (re.match(pattern['CR'],instruction)):
            self.CompareReg(address)
        elif (re.match(pattern['BT'],instruction)):
            if self.Flag == True:
                self.ICValue = address
            else:
                self.incIC()
        elif (re.match(pattern['GD'],instruction)):
            self.SI = 1
        elif (re.match(pattern['PD'],instruction)):
            self.SI = 2
        elif (re.match(pattern['H'],instruction)):
            self.SI = 3
        else:
            self.PI = 1

    def decode(self):
        decodeList = []
    
        if 'h' in self.IR[0].lower():
            inst = self.IR[0]
            address = '00'
        else:
            inst = self.IR[0] + self.IR[1]
            
            address = self.IR[2] + self.IR[3]
    
        decodeList.append(inst)
        decodeList.append(address)
    
        return decodeList

    def Process(self):
        '''
            Execute the user program.

            Fetch
            Decode
            Execute
            Check For interrupts
        '''
        #address = None
        #inst = None

        if not self.currentProgram == None:
            self.IC = self.currentProgram.IC
            while (not (self.halt or self.currentProgram == None)):
                self.currentProgram.TTC += 1
                if(self.currentProgram.TTC > self.currentProgram.TTL):
                    self.TI = 2
                RA = Memory.UserStorage.MapAddress(self.ICValue,self,self.currentProgram)
                if(self.PI == 3):
                    self.MasterMode('inst',RA)
                    continue
                self.IRValue = Memory.UserStorage.MemoryList[RA]
                self.incIC()
                instruction = self.decode()[0]
                address = Memory.UserStorage.MapAddress(self.decode()[1],self,self.currentProgram)
                if(self.PI == 2 or self.PI == 3):
                    self.MasterMode(instruction,address)
                    continue
                self.execute(instruction,address)
                self.MasterMode(instruction,address)

        size = SystemQueue.ReadyQueue.qsize()
        if self.currentProgram == None:
            if not SystemQueue.ReadyQueue.empty():
                self.currentProgram = SystemQueue.ReadyQueue.get()


        #if not SystemQueue.ReadyQueue.empty() and self.currentProgram == None:
        #    self.currentProgram = SystemQueue.ReadyQueue.get()

    def IOInterrupt(self):

        if self.IOI > 0:
            if self.IOI == 1:
                self.IR1()
            elif self.IOI == 2:
                self.IR2()
            elif self.IOI == 3:
                self.IR2()
                self.IR1()
            elif self.IOI == 4:
                self.IR3()
            elif self.IOI == 5:
                self.IR1()
                self.IR3()
            elif self.IOI == 6:
                self.IR3()
                self.IR2()
            elif self.IOI == 7:
                self.IR2()
                self.IR1()
                self.IR3()

    def MasterMode(self,inst,location):
        '''
        '''
        
        if self.TI == 0 or self.TI == 1:
            if self.PI == 1:
                self.Abort(5)
                self.PI = 0
            elif self.PI == 2:
                self.Abort(6)
                self.PI = 0
            elif self.PI == 3:
                if inst.lower() in self.readInst:
                    self.Abort(7)
                    self.PI = 0
                elif inst.lower() in self.writeInst:
                    pg = Memory.UserStorage.AllocatePage()
                    Memory.UserStorage.updateTable(pg,location,self.currentProgram)
                    self.decIC()
                    self.PI = 0
            elif self.SI == 1:
                self.currentProgram.IOReadLoc = roundOff(location)
                self.currentProgram.IC = self.IC
                ioRPcb = self.currentProgram
                SystemQueue.IOReadQueue.put(ioRPcb)
                self.currentProgram = None
                self.SI = 0
            elif self.SI == 2:
                self.currentProgram.IOWriteLoc = roundOff(location)
                self.currentProgram.OPCounter += 1
                self.currentProgram.IC = self.IC
                self.currentProgram.TLC += 1
                ioWPcb = self.currentProgram
                SystemQueue.IOWriteQueue.put(ioWPcb)
                self.currentProgram = None
                #PutData(location,self,self.currentProgram,Memory)
                self.SI = 0
            elif self.SI == 3:
                self.Abort(1)
                self.SI = 0
            
        elif self.TI == 2:
            if self.PI == 1:
                self.Abort(4,5)
                self.PI = 0
                self.TI = 0
            elif self.PI == 2:
                self.Abort(4,6)
                self.PI = 0
                self.TI = 0
            elif self.PI == 3:
                self.Abort(4)
                self.PI = 0
                self.TI = 0
            elif self.SI == 1:
                self.Abort(4)
                self.SI = 0
                self.TI = 0
            elif self.SI == 2:
                self.currentProgram.IOWriteLoc = roundOff(location)
                self.OPCounter += 1
                self.currentProgram.IC = self.IC
                self.currentProgram.TLC += 1
                ioWPcb = self.currentProgram
                SystemQueue.IOWriteQueue.put(ioWPcb)
                self.currentProgram = None
                #PutData(location,self,self.currentProgram,Memory)
                self.SI = 0
                self.TI = 0
                self.Abort(4)
            elif self.SI == 3:
                self.Abort(1)
                self.SI = 0
                self.TI = 0
            else:
                self.Abort(4)
                self.TI = 0
        else:
            print 'No interrupt raised'


    def Abort(self,*args,**kwargs):
        self.currentProgram.terminated = True
        endedProg = self.currentProgram
        SystemQueue.TerminateQueue.put(endedProg)
        

        if 1 in args:
            Logger.enterLog('Process- '+ str(self.currentProgram.PID) + ': Program Halt Encountered')
            print 'Program Halt Encountered'
        if 2 in args:
            Logger.enterLog('Process- ' + str(self.currentProgram.PID) + ': something')
            print 'something'
        if 3 in args:
            Logger.enterLog('Process- ' + str(self.currentProgram.PID) +': Line Limit Exceeded')
            print 'Line Limit Exceeded'
        if 4 in args:
            Logger.enterLog('Process- ' + str(self.currentProgram.PID) + ': Time Limit of program exceeded.. Program Ending...')
            print 'Time Limit of program exceeded.. Program Ending...'
        if 5 in args:
            Logger.enterLog('Process- ' + str(self.currentProgram.PID) + ': Operation Error Occured program ending...')
            print 'Operation Error Occured program ending...'
        if 6 in args:
            Logger.enterLog('Process- ' + str(self.currentProgram.PID) + ': Invalid operand passed. Program Ending...')
            print 'Invalid operand passed. Program Ending...'
        if 7 in args:
            Logger.enterLog('Process- ' + str(self.currentProgram.PID) + ': Invalid Page Fault Occured. Program Ending...')
            print 'Invalid Page Fault Occured. Program Ending...'

        self.currentProgram = None


    def IR1(self):
        channel.channel1.run()
        self.IOI -= 1
        channel.channel1.timer = 0

    def IR2(self):
        channel.channel2.run()
        self.IOI -= 2
        channel.channel2.timer = 0

    def IR3(self):
        channel.channel3.run()
        self.IOI -= 4
        channel.channel3.timer = 0

    def Reset(self):
        del(self.Register[:])
        self.resetIC()
        self.Flag = False
        del(self.IR[:])
        self.interruptvalidator = 0
        self.halt = 0