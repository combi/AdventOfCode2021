# import fileinput  # TODO(tester ce module)
# import collections
import os
# import sys
import glob
import re
import time

def timeIt(func):
    def func_decorated(*args, **kwargs):
        startTime = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time()-startTime
        print '[%s time] (%ss)' %(func.__name__, elapsed)
        return result

    return func_decorated


class Grid(object):
    def __init__(self, lines):

        self.lines = [set(x) for x in lines]
        self.cols  = [set(x) for x in zip(*lines)]
        self.bingo = None


    def check(self, num, verbose=False):
        bingo = False
        for line in self.lines:
            line.discard(num)
            if not line:
                bingo = True
                break

        if not bingo:
            for col in self.cols:
                col.discard(num)
                if not col:
                    bingo = True

        if bingo:
            self.bingo = sum([sum(l) for l in self.lines]) * num

            if verbose:
                if self.bingo:
                    print "BIIIINNGOOOOOOOOOOOOOOObingo"
                for line in self.lines:
                    print line
                print 'bingo =', self.bingo

            return self.bingo



    def test(self):
        bingo = sum([sum(l) for l in self.lines])
        print 'bingo =', bingo
        return

def getData(inputFile):
    with open(inputFile, 'r') as f:
        inputDataRaw = [x.strip() for x in f.readlines() if x and not x.startswith('#')]

    numSeq = eval(inputDataRaw[0])

    grids = []

    for i, line in enumerate(inputDataRaw[2::6]):
        gl1 = tuple( [int(x) for x in re.findall(r'\d+', inputDataRaw[2+(i*6)+0])] )
        gl2 = tuple( [int(x) for x in re.findall(r'\d+', inputDataRaw[2+(i*6)+1])] )
        gl3 = tuple( [int(x) for x in re.findall(r'\d+', inputDataRaw[2+(i*6)+2])] )
        gl4 = tuple( [int(x) for x in re.findall(r'\d+', inputDataRaw[2+(i*6)+3])] )
        gl5 = tuple( [int(x) for x in re.findall(r'\d+', inputDataRaw[2+(i*6)+4])] )

        grids.append(Grid(lines=(gl1,gl2,gl3,gl4,gl5)))

    return numSeq, grids


@timeIt
def part1(inputData):
    """
    """
    result = 0
    numSeq, grids = inputData
    for num in numSeq:
        for grid in grids:
            grid.check(num)
            if grid.bingo:
                return grid.bingo

    return result

@timeIt
def part2(inputData, verbose=False):
    """
    """
    result = 0
    numSeq, grids = inputData

    numSeq, grids = inputData
    winningGrids = []
    for num in numSeq:
        for grid in grids:
            if grid.bingo:
                continue
            grid.check(num)
            if grid.bingo:
                winningGrids.append(grid)

    result = winningGrids[-1].bingo
    return result

def gogo(verbose=False, part1Test=False, part1Final=False, part2Test=False, part2Final=False):
    location     = os.path.dirname(__file__)
    current      = os.path.basename(__file__).split('.')[0]
    part1_inputs = glob.glob('%s/%s_part1_data.txt' %(location, current))
    part1_tests  = glob.glob('%s/%s_part1_sample*.txt' %(location, current))
    part2_inputs = glob.glob('%s/%s_part2_data.txt' %(location, current))
    part2_tests  = glob.glob('%s/%s_part2_sample*.txt' %(location, current))

    if part1Test:
        print 'PART 1 TESTS ------------------------------------'
        expectedResult = 4512
        for inputFile in part1_tests:
            print inputFile
            inputData = getData(inputFile)
            result = part1(inputData)
            print 'result =', result, result == expectedResult
            print

    if part1Final:
        expectedResult = 38913
        expectedResult = 38913
        print 'PART 1 FINAL ------------------------------------'
        for inputFile in part1_inputs:
            print inputFile
            inputData = getData(inputFile)
            result = part1(inputData)
            print 'result =', result, result == expectedResult
            print


    if part2Test:
        expectedResult = 1924
        print 'PART 2 TESTS ------------------------------------'
        for inputFile in part2_tests:
            print inputFile
            inputData = getData(inputFile)
            result = part2(inputData, verbose=verbose)
            print 'result =', result, result == expectedResult
            print

    if part2Final:
        print 'PART 2 FINAL ------------------------------------'
        expectedResult = 16836
        for inputFile in part2_inputs:
            print inputFile
            inputData = getData(inputFile)
            result = part2(inputData, verbose=verbose)  # Ma version
            print 'result =', result, result == expectedResult
            print



def test():
    # ----------------------------
    # l1 = [1,2,3,4,5,6]
    # l2 = ['a','b','c','d','e','f']
    # l3 = ['A','B','C','D','E','F']

    # z1 = zip(l1, l2, l3)
    # print 'z1 =', z1
    # z2 = zip(*z1)
    # print 'z2 =', z2
    # ----------------------------
    l1 = [1,2,3]
    l2 = [4,5,6]
    l3 = [7,8,9]
    g = Grid(lines=(l1, l2, l3))
    # print 'g =', g
    # g.test()
    # print sum(range(10))
    print '\ncheck1:'
    g.check(1, verbose=True)
    print '\ncheck2:'
    g.check(4, verbose=True)
    print '\ncheck3:'
    g.check(5, verbose=True)
    print '\ncheck4:'
    g.check(7, verbose=True)
    print '\ncheck5:'
    g.check(8, verbose=True)
    print '\ncheck6:'
    g.check(6, verbose=True)


if __name__=="__main__":
    # print(sys.version)
    gogo(verbose=False, part1Test=False, part1Final=False, part2Test=True, part2Final=True)
    # test()
