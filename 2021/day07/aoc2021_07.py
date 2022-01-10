# import fileinput  # TODO(tester ce module)
import collections
import os
import sys
import glob
import re
import time

EXPECTED_TEST1  = 37
EXPECTED_FINAL1 = 344735
EXPECTED_TEST2  = 168
EXPECTED_FINAL2 = 96798233

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

def cumulateFuel(crabsCounts, verbose=False):

    cumul  = dict()

    prevPos   = crabsCounts[0][0]
    prevCrabs = crabsCounts[0][1]
    prevFuel  = 0

    cumul[prevPos] = prevFuel

    for posHere, crabsHere in crabsCounts[1:]:
        distToHere = abs(posHere - prevPos)

        fuelHere = (distToHere*prevCrabs) + prevFuel

        if verbose:
            print
            print 'Pos Here %d' %posHere
            print 'Crabs Here %d' %crabsHere
            print 'distToHere = ', distToHere
            print 'prevCrabs  = ', prevCrabs
            print 'prevFuel   = ', prevFuel
            print 'cumulated fuel to here: (%d x %d) + %d = %d' %(distToHere, prevCrabs, prevFuel, fuelHere)
        cumul[posHere] = fuelHere
        prevCrabs += crabsHere
        prevFuel  = fuelHere
        prevPos = posHere

    if verbose:
        print '\n'*5
        for pos, (fuel) in sorted(cumul.items()):
            print 'At %d, %d fuel' %(pos, fuel)

    return cumul

def cumulateFuel2(crabsCounts, verbose=False):

    cumul  = dict()
    for posHere, crabsHere in crabsCounts:
        cumul[posHere] = fuelToPos(posHere, crabsCounts)

    if verbose:
        print '\n'*5
        for pos, (fuel) in sorted(cumul.items()):
            print 'At %d, %d fuel' %(pos, fuel)

    return cumul

def fuelToPos(pos, crabsCounts, verbose=False):

    fuelTotal = 0
    for crabsPos, crabsNum in crabsCounts:
        distToHere = abs(crabsPos - pos)
        fuelTotal += (sum(range(distToHere+1))*crabsNum)

    return fuelTotal

@timeIt
def part1(inputData, verbose=False):
    """
    """
    result = 0

    crabsCounts = collections.Counter(inputData)
    sortedCrabsCounts = sorted(crabsCounts.items())
    backwards = cumulateFuel(sortedCrabsCounts[::-1])
    forwards  = cumulateFuel(sortedCrabsCounts)

    if verbose:
        print 'inputData         = ', inputData
        print 'sortedCrabsCounts = ', sortedCrabsCounts
        print 'forwards          = ', forwards
        print 'backwards         = ', backwards


    fuelCostsAtEachPos = dict()
    for pos in crabsCounts:
        fuelCostsAtEachPos[pos] = forwards.get(pos) + backwards.get(pos)

    # print 'fuelCostsAtEachPos =', fuelCostsAtEachPos
    minCost = sorted(fuelCostsAtEachPos.items(), key=lambda x:x[1])
    # print 'minCost =', minCost
    result = minCost[0][1]
    return result

@timeIt
def part2(inputData, verbose=False):
    """
    """
    result = 0
    result = 0

    crabsCounts = collections.Counter(inputData)
    sortedCrabsCounts = sorted(crabsCounts.items())
    cumulated  = cumulateFuel2(sortedCrabsCounts, verbose=False)

    cumulatedList = cumulated.items()

    if verbose:
        print 'inputData         = ', inputData
        print 'sortedCrabsCounts = ', sortedCrabsCounts

        print '\n'*5
        print 'cumulated:'
        for pos, fuel in sorted(cumulatedList):
            # print 'At %d, %d crabs, %d fuel' %(pos, fuel)
            print 'At %d, %d fuel' %(pos, fuel)

    minCost = sorted(cumulatedList, key=lambda x:x[1])
    index = cumulatedList.index(minCost[0])
    itemBefore = cumulatedList[index-1]
    itemAfter = cumulatedList[index+1]


    posRange = range(itemBefore[0], itemAfter[0])
    fuels = [fuelToPos(p, sortedCrabsCounts) for p in posRange]

    minCost = min(fuels)
    result = minCost

    return result


def test():
    # inputData = [16,1,2,0,4,2,7,1,2,14]
    # inputData = [160,1,2,0,4,2,7,1,2,14]
    # # inputData = [16,16,16,16,16,1]qqes temps
    # # inputData = [16,11,8,13,9,11,9,13,15,7,7,9,11,15,16,15,11,8,9,13,14,14,11,8,13]
    # counts = collections.Counter(inputData)
    # print 'counts.values() =', counts.values()
    # for k,v in sorted(counts.items(), key=lambda x:x[0]):
    #     print '%s:%s' %(k,v)



    # weightedAverage = 0.0
    # for value, occurences in counts.items():
    #     weightedAverage += value*occurences
    # weightedAverage/= sum(counts.values())
    # print 'weightedAverage =', weightedAverage
    # print 'xMean =', xMean
    # -----------------------------------------------

    # inputData = [16,1,2,0,4,2,7,1,2,14]
    # xMean = sum(inputData)/len(inputData)
    # print 'xMean =', xMean

    # numerator = 0
    # denominator = 0
    # for x in inputData:
    #     xx = x-xMean
    #     numerator += xx
    #     denominator += (xx*xx)
    # print 'numerator =', numerator
    # print 'denominator =', denominator

    # m = numerator/denominator
    # print 'm =', m
    # -----------------------------------------------
    inputData = [16,1,2,0,4,2,7,1,2,14]
    # inputData = [0,1,1,3,7,7,7,7,7,9,9]
    # counts = sorted(collections.Counter(inputData).items())
    # print 'counts =', counts
    # cumulateFuel2(counts, verbose=True)
    print part2(inputData)


if __name__=="__main__":
    print(sys.version)
    gogo(verbose=False, part1Test=True, part1Final=True, part2Test=True, part2Final=True)
    # test()
