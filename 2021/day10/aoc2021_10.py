# import fileinput  # TODO(tester ce module)
# import collections
import os
import sys
import glob
# import re
import time

EXPECTED_TEST1  = 26397
EXPECTED_FINAL1 = 316851
EXPECTED_TEST2  = 288957
EXPECTED_FINAL2 = 2182912364

def gogo(verbose=False, part1Test=False, part1Final=False, part2Test=False, part2Final=False):
    location     = os.path.dirname(__file__)
    current      = os.path.basename(__file__).split('.')[0]
    part1_inputs = glob.glob('%s/%s_part1_data.txt' %(location, current))
    part1_tests  = glob.glob('%s/%s_part1_sample*.txt' %(location, current))
    part2_inputs = glob.glob('%s/%s_part2_data.txt' %(location, current))
    part2_tests  = glob.glob('%s/%s_part2_sample*.txt' %(location, current))

    if part1Test:
        print 'PART 1 TESTS ------------------------------------'
        for inputFile in part1_tests:
            print inputFile
            inputData = getData(inputFile)
            result = part1(inputData)
            print 'result =', result, result == EXPECTED_TEST1
            print

    if part1Final:
        print 'PART 1 FINAL ------------------------------------'
        for inputFile in part1_inputs:
            print inputFile
            inputData = getData(inputFile)
            result = part1(inputData)
            print 'result =', result, result == EXPECTED_FINAL1
            print


    if part2Test:
        print 'PART 2 TESTS ------------------------------------'
        for inputFile in part2_tests:
            print inputFile
            inputData = getData(inputFile)
            result = part2(inputData, verbose=verbose)
            print 'result =', result, result == EXPECTED_TEST2
            print

    if part2Final:
        print 'PART 2 FINAL ------------------------------------'
        for inputFile in part2_inputs:
            print inputFile
            inputData = getData(inputFile)
            result = part2(inputData, verbose=verbose)  # Ma version
            print 'result =', result, result == EXPECTED_FINAL2
            print

def timeIt(func):
    def func_decorated(*args, **kwargs):
        startTime = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time()-startTime
        print '[%s time] (%ss)' %(func.__name__, elapsed)
        return result

    return func_decorated

def getData(inputFile):
    with open(inputFile, 'r') as f:
        inputDataRaw = [x.strip() for x in f.readlines() if x and not x.startswith('#')]
    inputData = inputDataRaw
    return inputData

ILLEGALPOINTS = {')': 3 ,
                 ']': 57 ,
                 '}': 1197 ,
                 '>': 25137}

COMPLETEPOINTS = {')': 1 ,
                  ']': 2 ,
                  '}': 3 ,
                  '>': 4}


SYMBOLS = {'(':')',
           ')':'(',
           '[':']',
           ']':'[',
           '{':'}',
           '}':'{',
           '<':'>',
           '>':'<'}

opened = set(['(','[','{','<'])
closed = set([')',']','}','>'])


class Chunk(object):
    def __init__(self, ident, parent=None):
        self.openSymbol  = ident
        self.closeSymbol = SYMBOLS[ident]
        self.isClosed    = False

    def __str__(self):
        return self.openSymbol+self.closeSymbol

    def __repr__(self):
        return self.openSymbol+self.closeSymbol

def printChunks(chunks, printIt=True):
    chunksStr = str(chunks)
    result = chunksStr[1:-1]
    if printIt:
        print result
    return result


@timeIt
def parse(inputData, getCorruptScore=False, getCompleteScore=False, verbose=False):
    """
    """
    # print 'inputData =', inputData
    result = None
    corruptScore  = 0
    completeScore = 0

    completeScores = []

    for line in inputData:
        chunks = []
        if verbose:
            print '\n'
            print 'line =', line
        illegal = None
        # corruptScore = 0
        line_completeScore = 0

        for i, symbol in enumerate(line):
            symbolStatus = 'is opening' if symbol in opened else 'is closing'
            if verbose:
                print
                print '  %s' %line
                print '  %s^ %s' %((' '*i), symbolStatus)
                print '    chunks at start :', printChunks(chunks, printIt=False)
            closedChunk = None
            if symbol in opened:
                chunks.append(Chunk(symbol))
            elif symbol in closed:
                for _chk in chunks[::-1]:
                    if verbose: print '    _chk =', _chk
                    if _chk.closeSymbol == symbol:
                        _chk.isClosed = True
                        closedChunk = _chk
                        if verbose: print 'breaking A'
                        break
                    elif not _chk.isClosed:
                        illegal = symbol
                        if verbose: print 'breaking B'
                        break
            if illegal:
                if verbose: print 'breaking C'
                corruptScore+=ILLEGALPOINTS[symbol]
                break
            elif closedChunk:
                chunks.pop()
            if verbose: print '    chunks at end   :', printChunks(chunks, printIt=False)

        if not illegal:
            for chunk in chunks[::-1]:
                line_completeScore *= 5
                line_completeScore += COMPLETEPOINTS[chunk.closeSymbol]
            completeScores.append(line_completeScore)


    completeScores.sort()
    i = len(completeScores)//2
    completeScore = completeScores[i]

    if verbose:
        print 'corruptScore =', corruptScore
        print 'completeScore =', completeScore

    if getCompleteScore and getCorruptScore:
        result = (completeScore, corruptScore)
    elif getCompleteScore:
        result = completeScore
    elif getCorruptScore:
        result = corruptScore

    return result

def part1(inputData, verbose=False):
    return parse(inputData, verbose=verbose, getCorruptScore=True, getCompleteScore=False)

def part2(inputData, verbose=False):
    return parse(inputData, verbose=verbose, getCorruptScore=False, getCompleteScore=True)



if __name__=="__main__":
    print(sys.version)
    # gogo(verbose=False, part1Test=True)
    # gogo(verbose=False, part1Final=True)
    gogo(verbose=False, part2Test=True)
    gogo(verbose=False, part2Final=True)
