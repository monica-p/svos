from Memory import Memory
from globalHelp import *
from SystemQueue import SystemQueue
from CPU import CPU
from Printer import Printer
from Logger import Logger
#---------------------------- Global Variables ----------------------------------------------


CPU = CPU()

Memory.initialise()
SystemBuffer.initialise()
Printer.initialize()
Logger.initialize()

def main():
    channel.channel1.ChannelBusy = True
    channel.channel3.ChannelBusy = True
    channel.channel2.ChannelBusy = True

    while(not channel.ChannelIdle()):
        simulate()
        CPU.Process()
        CPU.IOInterrupt()


def simulate():
    busyList = []
    for ch in channel.channelList:
        if ch.ChannelBusy:
            busyList.append(ch)
    
    channel.incChannelTimer(busyList)

    for ch in channel.channelList:
        if ch.timer == ch.totalTime:
            if ch.ChannelName == 'channel1':
                CPU.IOI = CPU.IOI + 1
            elif ch.ChannelName == 'channel2':
                CPU.IOI = CPU.IOI + 2
            elif ch.ChannelName == 'channel3':
                CPU.IOI = CPU.IOI + 4


main()
Memory.AuxillaryStorage.show()