# import fileinput  # TODO(tester ce module)
import collections
import os
import sys
import glob
import re
import time

EXPECTED_TEST1  = 5934
EXPECTED_FINAL1 = 352872
EXPECTED_TEST2  = 26984457539
EXPECTED_FINAL2 = 1604361182149


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
        inputDataRaw = [x.strip() for x in f.readlines() if x and not x.startswith('#')][0]

    inputData = [int(x) for x in re.findall(r'-?\d+', inputDataRaw)]
    return inputData

def growFishes(fishes, numDays, verbose=False):
    def printFishes(fishes):
        toPrint = ''
        totalFishes = countFishes(fishes)
        for _, numFishes in sorted(fishes.items()):
            toPrint += '%d ' %numFishes
        print '%d fishes: %s' %(totalFishes, toPrint)

    def countFishes(fishes):
        result = 0
        for _, numFishes in fishes.items():
            result += numFishes
        return result

    result = 0

    maxDays = numDays
    day     = 0

    if verbose:
        print '====================='
        print 'day = 0'
        for fishTime, numFishes in fishes.items():
            print '%d fishes are at time %d' %(numFishes, fishTime)
        printFishes(fishes)
        print '====================='
        print

    while day < maxDays:
        day += 1
        if verbose:
            print '----------------'
            print 'day =', day
        fishes0 = fishes[0]
        for fishTime, numFishes in sorted(fishes.items()):
            newFishTime = fishTime-1 if fishTime>0 else 8
            fishes[newFishTime] = numFishes
        fishes[6]+=fishes0

        if verbose: printFishes(fishes)

    result = countFishes(fishes)
    print 'result =', result

    return result


@timeIt
def part1(inputData, verbose=False):
    """
    """
    result = 0
    fishes = collections.Counter(dict((x, 0) for x in range(9)))
    fishes.update(inputData)
    result = growFishes(fishes, 80, verbose=verbose)
    return result

@timeIt
def part2(inputData, verbose=False):
    """
    """
    result = 0
    fishes = collections.Counter(dict((x, 0) for x in range(9)))
    fishes.update(inputData)
    result = growFishes(fishes, 256)
    return result


def test():
    # counts = dict((x, 0) for x in range(9))
    col = collections.Counter(dict((x, 0) for x in range(9)))
    print 'col =', col
    bob = [1,2,2,3,3,3,4,4,4,4]
    col.update(bob)
    print 'col =', col


if __name__=="__main__":
    print(sys.version)
    gogo(verbose=False, part1Test=True, part1Final=True, part2Test=True, part2Final=True)
    # test()
