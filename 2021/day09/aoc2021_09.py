# import fileinput  # TODO(tester ce module)
# import collections
import os
import sys
import glob
# import re
import time

EXPECTED_TEST1  = 15
EXPECTED_FINAL1 = 532
EXPECTED_TEST2  = 1134
EXPECTED_FINAL2 = 1110780


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
    result = list()

    x, y = cell
    if x > 0:
        # result.add((y,x-1))
        result.append((x-1, y))
    if x < xLimit-1:
        # result.add((y,x+1))
        result.append((x+1, y))
    if y > 0:
        # result.add((y-1,x))
        result.append((x, y-1))
    if y < yLimit-1:
        # result.add((y+1,x))
        result.append((x, y+1))
    return result


def getHeightAtCell(grid, cell):
    return grid[cell[1]][cell[0]]


@timeIt
def part1(inputData, verbose=False):
    """
    """
    result = 0

    grid = inputData
    WIDTH  = len(grid[0])
    HEIGHT = len(grid)
    if verbose:
        print 'WIDTH  =', WIDTH
        print 'HEIGHT =', HEIGHT

    lowPoints = []

    for y in range(HEIGHT):
        for x in range(WIDTH):
            cell = (x, y)
            h = grid[y][x]
            nbh = set(getAdjacentHeights(grid, cell, WIDTH, HEIGHT))

            if h == 0 or h < min(nbh):
                lowPoints.append(h)
    if verbose: print 'lowPoints =', lowPoints
    result = sum([x+1 for x in lowPoints])
    return result

@timeIt
def part2(inputData, verbose=False):
    """
    """
    result = 0
    grid = inputData

    WIDTH  = len(grid[0])
    HEIGHT = len(grid)
    if verbose:
        print 'WIDTH  =', WIDTH
        print 'HEIGHT =', HEIGHT
        for l in grid:
            print l

    lowPoints = []

    for y in range(HEIGHT):
        for x in range(WIDTH):
            cell = (x, y)
            h = grid[y][x]

            nbh = getAdjacentHeights(grid, cell, WIDTH, HEIGHT)
            if h == 0 or h < min(nbh):
                lowPoints.append((x,y))

    if verbose: print 'lowPoints =', lowPoints
    lowHs = [grid[y][x] for (x,y) in lowPoints]
    result = sum([x+1 for x in lowHs])


    if False:
        strMap = []

        for y in range(HEIGHT):
            line = ''
            for x in range(WIDTH):
                if (x,y) in lowPoints:
                    line += '@'
                else:
                    line += str(grid[y][x])
            strMap.append(line)
        for x in strMap:
            print x

    basins = []
    for lowCell in lowPoints:
        basin = set()
        pool = set([lowCell])
        if verbose:
            print
            print 'lowCell =', lowCell
            print 'pool    =', pool
        iters  = 0
        safety = 1500
        while pool and safety:
            safety -= 1
            iters += 1
            cell = pool.pop()
            # nbc = set(getAdjacentCells(inputData, cell, WIDTH, HEIGHT))
            nbc = set([c for c in getAdjacentCells(inputData, cell, WIDTH, HEIGHT) if not getHeightAtCell(grid, c)==9]) - basin
            if verbose:
                print
                print '  cell  =', cell
                print '  pool  =', pool
                print '  nbc   =', nbc
            basin.add(cell)
            pool.update(nbc)
            if verbose:

                print '  pool  =', pool
                print '  basin =', basin
        basins.append(basin)

    basinsSizes = sorted([len(b) for b in basins], reverse=True)
    result = 1
    for x in basinsSizes[0:3]:
        result *= x

    return result


def makeStrGrid(grid, gridMask=None):
    # inputData = getData('/home/combi/DEV/PYTHON/AdventOfCode/2021/day09/aoc2021_09_part1_sample1.txt')
    strGrid = []
    for l in grid:
        # print l
        q = ''.join([str(x) for x in l])
        # print 'q =', q
        strGrid.append(q)

    return strGrid

def test():
    inputData = getData('/home/combi/DEV/PYTHON/AdventOfCode/2021/day09/aoc2021_09_part1_sample1.txt')

    WIDTH  = len(inputData[0])
    HEIGHT = len(inputData)
    print 'WIDTH =', WIDTH
    print 'HEIGHT =', HEIGHT
    cell = (1,0)
    nbc = getAdjacentCells(inputData, cell, WIDTH, HEIGHT)
    nbh = getAdjacentHeights(inputData, cell, WIDTH, HEIGHT)
    print 'cell =', cell
    print 'nbc  =', nbc
    print 'nbh  =', nbh

if __name__=="__main__":
    print(sys.version)
    gogo(verbose=False, part1Test=True, part1Final=True, part2Test=True, part2Final=True)
    # test()
