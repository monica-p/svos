from SystemQueue import  SystemQueue


class Buffer(object):
    """description of class"""

    def __init__(self):
        self.buffer = list(list())
        self.bufferType = str()

    def initialise(self):
        for i in range(0,1000):
            emptyBuffer = Buffer()
            emptyBuffer.Type = 'Empty'
            SystemQueue.EmptyBufferQueue.put(emptyBuffer)

    @property
    def Type(self):
        return self.bufferType

    @Type.setter
    def Type(self,value):
        self.bufferType = value

    def LoadBuffer(self,card):
        self.buffer = card

    def UnloadBuffer(self):
        return self.buffer

    def BufferShow(self):
        print self.buffer



