# import fileinput  # TODO(tester ce module)
# import collections
import os
import sys
import glob
# import re
import time

def timeIt(func):
    def func_decorated(*args, **kwargs):
        startTime = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time()-startTime
        print '[%s time] (%ss)' %(func.__name__, elapsed)
        return result

    return func_decorated



@timeIt
def part1(inputData):
    """
    """
    result = 0

    H = 0
    D = 0
    # print 'inputData =', inputData
    for move in inputData:
        direction = move[0]
        amount = int(move[1])
        if direction == 'forward':
            H+=amount
        elif direction == 'down':
            D+=amount
        elif direction == 'up':
            D-=amount
    result = H*D
    return result

@timeIt
def part2(inputData, verbose=False):
    """
    """
    result = 0

    H = 0
    D = 0
    A = 0

    # print 'inputData =', inputData
    for move in inputData:
        direction = move[0]
        amount = int(move[1])
        if direction == 'forward':
            H+=amount
            D += A*amount
        elif direction == 'down':
            A+=amount
        elif direction == 'up':
            A-=amount
    if verbose:
        print 'H =', H
        print 'D =', D
        print 'A =', A
    result = H*D
    return result


def getData(inputFile):
    with open(inputFile, 'r') as f:
        inputData = [l.strip().split(' ') for l in f.readlines() if l and not l.startswith('#')]
        return inputData


def gogo(verbose=False, part1Test=False, part1Final=False, part2Test=False, part2Final=False):
    location     = os.path.dirname(__file__)
    current      = os.path.basename(__file__).split('.')[0]
    part1_inputs = glob.glob('%s/%s_part1_data.txt' %(location, current))
    part1_tests  = glob.glob('%s/%s_part1_sample*.txt' %(location, current))
    part2_inputs = glob.glob('%s/%s_part2_data.txt' %(location, current))
    part2_tests  = glob.glob('%s/%s_part2_sample*.txt' %(location, current))

    if part1Test:
        expectedResult = 150
        print 'PART 1 TESTS ------------------------------------'
        for inputFile in part1_tests:
            print inputFile
            inputData = getData(inputFile)
            result = part1(inputData)
            print 'result =', result, result == expectedResult
            print

    if part1Final:
        expectedResult = 1855814
        print 'PART 1 FINAL ------------------------------------'
        for inputFile in part1_inputs:
            print inputFile
            inputData = getData(inputFile)
            result = part1(inputData)
            print 'result =', result, result == expectedResult
            print


    if part2Test:
        expectedResult = 900
        print 'PART 2 TESTS ------------------------------------'
        for inputFile in part2_tests:
            print inputFile
            inputData = getData(inputFile)
            result = part2(inputData, verbose=verbose)
            print 'result =', result, result == expectedResult
            print

    if part2Final:
        expectedResult = 1845455714
        print 'PART 2 FINAL ------------------------------------'
        for inputFile in part2_inputs:
            print inputFile
            inputData = getData(inputFile)
            result = part2(inputData, verbose=verbose)  # Ma version
            print 'result =', result, result == expectedResult
            print


if __name__=="__main__":
    print(sys.version)
    gogo(verbose=False, part1Test=True, part1Final=True, part2Test=True, part2Final=True)
