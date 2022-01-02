# import fileinput  # TODO(tester ce module)
import collections
import os
import sys
import glob
import re
import time

EXPECTED_TEST1  = 5
EXPECTED_FINAL1 = 6283
EXPECTED_TEST2  = 12
EXPECTED_FINAL2 = None


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
        inputDataRaw = [x for x in f.readlines() if x and not x.startswith('#')]

    inputData = []
    for line in inputDataRaw:
        coords = [int(x) for x in re.findall(r'-?\d+', line)]
        inputData.append(coords)

    # print 'inputData =', inputData

    return inputData

def isLineStraight(line):
    (x0,y0), (x1,y1) = line
    if x0==x1 or y0==y1:
        return True
    return False

def isLineDiagonal45(line):
    (x0,y0), (x1,y1) = line
    xDelta = abs(x1-x0)
    yDelta = abs(y1-y0)
    result = (xDelta==0) or (yDelta==0) or (xDelta==yDelta)
    # print
    # print 'line =', line
    # print 'xDelta =', xDelta
    # print 'yDelta =', yDelta
    # print 'result =', result
    return result

def coveredCells(line):
    (x0,y0), (x1,y1) = line

    cells = set()
    xmin = min(x0, x1)
    xmax = max(x0, x1)
    ymin = min(y0, y1)
    ymax = max(y0, y1)
    for x in range(xmin, xmax+1):
        for y in range(ymin, ymax+1):
            cells.add((x,y))
    return cells

def coveredCells_NEW(line):
    (x0,y0), (x1,y1) = line

    xDelta = x1-x0
    # print 'xDelta =', xDelta
    yDelta = y1-y0
    # print 'yDelta =', yDelta
    xIncr = xDelta/abs(xDelta) if xDelta else 0
    yIncr = yDelta/abs(yDelta) if yDelta else 0

    numCovered = max(abs(xDelta),abs(yDelta)) +1
    # print 'numCovered =', numCovered
    cells = set()
    for i in range(numCovered):
        # print i
        cell = (x0+(i*xIncr),y0+(i*yIncr))
        # print 'cell =', cell
        cells.add(cell)
    return cells

@timeIt
def part1(inputData, verbose=False):
    """
    """
    result = 0
    counts = collections.Counter()
    for x0,y0,x1,y1 in inputData:
        line = ((x0,y0), (x1,y1))
        isStraight = isLineStraight(line)

        if verbose:
            print
            print 'line =', line
            print 'isStraight =', isStraight

        if not isStraight:
            continue

        # coveredCells_ = coveredCells(line)
        coveredCells_ = coveredCells_NEW(line)
        if verbose: print 'coveredCells_ =', coveredCells_

        for cell in coveredCells_:
            counts[cell]+=1
    if verbose: print 'counts =', counts

    for _, count in counts.items():
        if count > 1:
            result+=1
    return result

@timeIt
def part2(inputData, verbose=False):
    """
    """
    result = 0
    counts = collections.Counter()
    for x0,y0,x1,y1 in inputData:
        line = ((x0,y0), (x1,y1))
        isDiag45 = isLineDiagonal45(line)

        if verbose:
            print
            print 'line =', line,  'isDiag45 =', isDiag45

        coveredCells_ = coveredCells_NEW(line)
        if verbose: print 'coveredCells_ =', coveredCells_

        for cell in coveredCells_:
            counts[cell]+=1

    if verbose: print 'counts =', counts

    for _, count in counts.items():
        if count > 1:
            result+=1
    return result


def test():
    # ----------------------------------------------------
    col = collections.Counter()
    print 'col =', col
    col['a']+=1
    print 'col =', col
    col[(5, 7)]+=1
    print 'col =', col

    # ----------------------------------------------------
    # print range(-10, 10)
    # print range(10, -10)

if __name__=="__main__":
    print(sys.version)
    gogo(verbose=False, part1Test=False, part1Final=True, part2Test=True, part2Final=True)
    # test()
