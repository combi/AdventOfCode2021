# import fileinput  # TODO(tester ce module)
# import collections
import os
# import sys
import glob
# import re
import time

EXPECTED_TEST1  = 1656
EXPECTED_FINAL1 = 1613
EXPECTED_TEST2  = 195
EXPECTED_FINAL2 = 510


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
    inputData = []
    with open(inputFile, 'r') as f:
        for l in f.readlines():
            if l.startswith('#'):
                continue
            d = [int(x) for x in l.strip()]
            inputData.append(d)

    return inputData

def getAdjacentHeights(grid, cell, xLimit, yLimit):
    result = list()
    x, y = cell
    if x > 0:
        result.append(grid[y][x-1])
    if x < xLimit-1:
        result.append(grid[y][x+1])
    if y > 0:
        result.append(grid[y-1][x])
    if y < yLimit-1:
        result.append(grid[y+1][x])
    return result


def getAdjacentCells(grid, cell, xLimit, yLimit):
    result = set()

    x, y = cell
    xMin = max(0,x-1)
    xMax = min(x+1+1, xLimit)
    yMin = max(0,y-1)
    yMax = min(y+1+1, yLimit)

    for x in range(xMin, xMax):
        for y in range(yMin, yMax):
            result.add((x, y))

    return result


def printGridCells(grid, cells):
    cells_ = cells or []
    grid_  = []
    WIDTH  = len(grid[0])
    HEIGHT = len(grid)

    for y in range(HEIGHT):
        newLine = ''
        for x in range(WIDTH):
            if (x, y) in cells_:
                newLine+=str(grid[y][x])
            else:
                newLine+='.'
        grid_.append(newLine)
    printGrid(grid_)

def printGrid(grid):
    WIDTH  = len(grid[0])
    HEIGHT = len(grid)

    print '  ' + ''.join([str(x) for x in range(WIDTH)])
    for y in range(HEIGHT):
        toPrint = '%s ' %y
        for x in range(WIDTH):
            toPrint+=str(grid[y][x])
        print toPrint
    print

def getEnergyAtCell(grid, cell):
    return grid[cell[1]][cell[0]]

def setEnergyAtCell(grid, cell, e):
    grid[cell[1]][cell[0]] = e

def growGridEnergy(grid):
    WIDTH  = len(grid[0])
    HEIGHT = len(grid)

    numFlashes = 0

    flashed = set()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            e = getEnergyAtCell(grid, (x, y))
            if e == 9:
                flashed.add((x, y))
            setEnergyAtCell(grid, (x, y), min(9, e+1))

    # print 'flashed:'
    # printGridCells(grid, flashed)

    pool = list(flashed)
    safety = 500
    while pool:
        safety -= 1
        if safety < 0:
            print 'HIT SAFETY !!!'
            break
        cell = pool.pop()
        adjCells = getAdjacentCells(grid, cell, WIDTH, HEIGHT)
        # print 'adjCells =', adjCells
        for adjCell in adjCells:
            adje = getEnergyAtCell(grid, adjCell)
            if adje == 9:
                if adjCell not in flashed:
                    flashed.add(adjCell)
                    pool.append(adjCell)
            setEnergyAtCell(grid, adjCell, min(9, adje+1))


    # print 'flashed:'
    # printGridCells(grid, flashed)


    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (x, y) in flashed:
                setEnergyAtCell(grid, (x, y), 0)

    numFlashes = len(flashed)
    return numFlashes

def doesAllGridFlash(grid):
    WIDTH  = len(grid[0])
    HEIGHT = len(grid)

    for y in range(HEIGHT):
        for x in range(WIDTH):
            e = getEnergyAtCell(grid, (x, y))
            if not e==0:
                return False

    return True

@timeIt
def part1(inputData, verbose=False):
    """
    """
    # print 'inputData =' , inputData

    result = 0
    grid   = inputData
    WIDTH  = len(grid[0])
    HEIGHT = len(grid)
    STEPS  = 100

    if verbose:
        print 'WIDTH  =', WIDTH
        print 'HEIGHT =', HEIGHT

    for i in range(STEPS):
        numFlashes = growGridEnergy(grid)
        result += numFlashes

        if verbose:
            printGrid(grid)

    if verbose:
        print 'finalGrid:'
        printGrid(grid)

    return result

@timeIt
def part2(inputData, verbose=False):
    """
    """

    result = 0
    grid   = inputData
    WIDTH  = len(grid[0])
    HEIGHT = len(grid)

    if verbose:
        print 'WIDTH  =', WIDTH
        print 'HEIGHT =', HEIGHT

    step = 0
    while not doesAllGridFlash(grid):
        step+=1
        growGridEnergy(grid)

    # print 'step =', step
    # printGrid(grid)

    result = step

    return result

def test():
    grid = [
        [5, 4, 8, 3, 1, 4, 3, 2, 2, 3],
        [2, 7, 4, 5, 8, 5, 4, 7, 1, 1],
        [5, 2, 6, 4, 5, 5, 6, 1, 7, 3],
        [6, 1, 4, 1, 3, 3, 6, 1, 4, 6],
        [6, 3, 5, 7, 3, 8, 5, 4, 7, 8],
        [4, 1, 6, 7, 5, 2, 4, 6, 4, 5],
        [2, 1, 7, 6, 8, 4, 1, 7, 2, 1],
        [6, 8, 8, 2, 8, 8, 1, 1, 3, 4],
        [4, 8, 4, 6, 8, 4, 8, 5, 5, 4],
        [5, 2, 8, 3, 7, 5, 1, 5, 2, 6],
    ]


    # -------------------------------------------------------------
    WIDTH  = len(grid[0])
    HEIGHT = len(grid)
    nbc = getAdjacentCells(grid, (1,0), WIDTH, HEIGHT)
    printGridCells(grid, nbc)
    nbc = getAdjacentCells(grid, (2,1), WIDTH, HEIGHT)
    printGridCells(grid, nbc)
    # -------------------------------------------------------------
    # printGrid(grid)

if __name__=="__main__":
    # print(sys.version)
    gogo(verbose=False, part1Test=True)
    gogo(verbose=False, part1Final=True)
    gogo(verbose=False, part2Test=True)
    gogo(verbose=False, part2Final=True)
    # test()

