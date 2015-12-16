from Printer import Printer

def MakeCard(WordList):
    '''
        
    '''
    WordCount = 0
    card = list(list())

    for i in range(0,len(WordList)):
        WordCount += 1
        card.append(WordList[i])
        if i == len(WordList) - 1 and WordCount < 10:
            while(WordCount != 10):
                card.append(['-','-','-','-'])
                WordCount += 1

    return card


def MakeWord(CharList):
    """

    """
    charCount = 0
    word = []
    wordList = list(list())

    for i in range(0,len(CharList)):
        charCount += 1
        word.append(CharList[i])
        if charCount == 4:
            wordList.append(word)
            charCount = 0
            word = []
        elif i == len(CharList) - 1 and charCount != 4:
            while(charCount != 4):
                word.append('-')
                charCount += 1
            wordList.append(word)

    return wordList

def filterList(argList):
    CharList = argList
    
    if (' ' in CharList):
        CharList = filter(lambda a: a != ' ',CharList)
    if ('' in CharList):
        CharList = filter(lambda a: a != '',CharList)
    if ('$' in CharList):
        CharList = filter(lambda a: a != '$',CharList)
    if ('\n' in CharList):
        CharList = filter(lambda a: a != '\n',CharList)
    if ('\r' in CharList):
        CharList = filter(lambda a: a != '\r',CharList)

    return CharList
                

def roundOff(address):
	if address % 10 != 0:
		index = address - (address % 10)
	else:
		index = address
	return index


def PutData(location,CPU,progPCB,Memory):

        progPCB.TLC += 1

        if(progPCB.TLC > progPCB.TLL):
                CPU.Abort(ProgFile,3)
        else:
            index = roundOff(location)
    
            data = ReadCard(index,Memory)
            if data == '0':
                print '		'
            else:
                print 'Data', data
                Printer.enterLog(str(progPCB.PID) + '-->' +'Data: ' + data)


def ReadCard(track):
        '''
            Read card from passed Memory Location.

            Para: Location to be Read ---> Returns: string to print (Card (10 word List))
        '''
        count = 0
        string = ''
    
        while(count < 10):
            string += ReadWord(track[count])
            if (string == '0'):
                break
            count += 1
        return string

def ReadWord(word):
        '''
            Read Word from passed Memory Location.

            Para: Location to be Read ---> Returns: Word (List of 4 char)
        '''
        if len(word) == 0:
            return '0'
        else:
            string = ''	
        
            for char in word:
                string += char
            return string
