import Queue

class SystemQueue(object):
    """description of class"""
    ReadyQueue = Queue.Queue()
    TerminateQueue = Queue.Queue()
    LoadQueue = Queue.Queue()
    IOReadQueue = Queue.Queue()
    IOWriteQueue = Queue.Queue()
    EmptyBufferQueue = Queue.Queue()
    InputBufferQueue = Queue.Queue()
    OutBufferQueue = Queue.Queue()
    USLoadQueue = Queue.Queue()

