"""
problem in understanding update page table and alocate page
prob in virtual address mapping
"""

class Memory(object):
    """description of class"""
    
    @classmethod
    def initialise(cls):
        Memory.AuxillaryStorage.AuxillaryStorageInit()
        Memory.UserStorage.UserStorageinitialise()

    class SupervisoryStorage(object):
        pass

    class AuxillaryStorage(object):
        
        
        Drum = list(list(list()))
        freeTrackArray = list()

        @classmethod
        def AuxillaryStorageInit(cls):
            for i in range(0,100):
                card = list(list())

                Memory.AuxillaryStorage.Drum.append(card)
                Memory.AuxillaryStorage.freeTrackArray.append(True)

        @classmethod
        def GetTrack(cls):
            
            freeTrackNo = 0

            for loop in range(0,100):
                if Memory.AuxillaryStorage.freeTrackArray[loop] == True:
                    freeTrackNo = loop
                    break
            Memory.AuxillaryStorage.freeTrackArray[freeTrackNo] = False
            return freeTrackNo

        @classmethod
        def GetTrackCard(cls,index):
            return Memory.AuxillaryStorage.Drum[index]

        @classmethod
        def clearTrack(cls,index):
            Memory.AuxillaryStorage.freeTrackArray[index] = True

        @classmethod
        def DrumFull(cls):
            pass

        @classmethod
        def show(cls):
            for card in Memory.AuxillaryStorage.Drum:
                print card

    class UserStorage(object):

        MemoryList = list(list())
        _FreeSpaceArray = list(list())


        @classmethod
        def UserStorageinitialise(cls):
            for i in range(0,300):
                Memory.UserStorage.MemoryList.append([])
            for j in range(0,30):
                Memory.UserStorage._FreeSpaceArray.append(True)

        @classmethod
        def clearArray(cls,index):
            Memory.UserStorage._FreeSpaceArray[index] = True

        
        
        @classmethod
        def LoadMemory(cls,Track,location):
            location *= 10

            for word in Track:
                Memory.UserStorage.MemoryList[location] = word
                location += 1

        @classmethod
        def ReadMemory(cls,location):
            memoryCard = list(list())
            counter = 0

            while(counter != 10):
                memoryCard.append(Memory.UserStorage.MemoryList[location])
                location += 1
                counter += 1

            return memoryCard




        @classmethod
        def GetMemoryLocation(cls):
            pass


        @classmethod
        def AllocatePage(cls):
            """
            choose a random no between 0,29
            if free mark occupied and return number
            if not keep searching
            """
            pageNo = 0

            for i in range(0,30):
                if Memory.UserStorage._FreeSpaceArray[i] == True:
                    Memory.UserStorage._FreeSpaceArray[i] = False
                    pageNo = i
                    break

            return pageNo

    
        @classmethod
        def updateTable(cls,pageNo,RA,ProcessPCB):
            try:
                index = ProcessPCB.PTR * 10 + (RA // 10)
                entry = []
                entry.append('-')
                entry.append('1')
                entry.append(str(pageNo//10))
                entry.append(str(pageNo % 10))
                Memory.UserStorage.MemoryList[index] = entry
                ProcessPCB.ProcessPageTable.append(entry)
            except Exception,err:
                print "Error in update table",err

        @classmethod
        def MapAddress(cls,strAddress,CPU,progPCB):
            """
            Method will convert the virtual address to real address using below formula :
		    indexAddress = (PTR*10) + TensPlaceLocation

            pick up page no from this index address from the table

		    RealAddress = (pageNo*10) + UnitsPlaceLocation

            convert str value of address to int
            check for valid address
                if 
                    not set PI = 2
                else
                    Map Adress
            Check Free space Array
            according to read or write operation set Page fault error
            Set interrupt accordingly (PI 2,3)
            """
            try:
                address = int(strAddress)
                indexAddress = progPCB.PTR * 10 + address//10

                entry = Memory.UserStorage.MemoryList[indexAddress]

            
                if len(entry) == 0 or entry[1] != '1':
                    CPU.PI = 3
                    return address
                else:
                    pageNo = Memory.UserStorage.MemoryList[indexAddress][2] + Memory.UserStorage.MemoryList[indexAddress][3]
                    RA = int(pageNo) * 10 + address % 10
                    #print 'real address',RA

                    if RA > 299:
                        CPU.PI = 2

                    return RA
            except Exception,err:
                CPU.PI = 2

        @classmethod
        def Show(cls):
            for word in UserStorage.MemoryList:
                print word
