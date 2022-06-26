# import fileinput  # TODO(tester ce module)
import collections

# import os
import sys
# import glob
# import re
import time

def go(goFunc, inputFile=None, expected=None, verbose=False):

    print
    print '-----------------------------------------------'
    print goFunc.__name__, inputFile
    inputData = getData(inputFile)

    startTime = time.time()
    result    = goFunc(inputData)
    elapsed   = time.time()-startTime

    print 'result =', result, result==expected
    print '(Elapsed %ss)' %elapsed
    # print '-----------------------------------------------'


def timeIt(func):
    def func_decorated(*args, **kwargs):
        startTime = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time()-startTime
        print '(Elapsed %ss)' %elapsed
        return result

    return func_decorated


def getData(inputFile):
    with open(inputFile, 'r') as f:
        inputDataRaw = [tuple(x.strip().split('-')) for x in f.readlines() if x and not x.startswith('#')]
    inputData = inputDataRaw
    return inputData

def isEndSegment(segment):
    return segment[1]=='end'

# @timeIt
def part1(inputData, verbose=False):
    """
    """
    print 'inputData =', inputData
    result = 0
    starts = set([x for x in inputData if 'start' in x])
    ends   = set([x for x in inputData if 'end' in x])
    others = set([x for x in inputData if x not in (starts | ends)])
    print 'starts =', starts
    print 'ends =', ends
    print 'others =', others

    linksTable = collections.defaultdict(set)
    for a,b in inputData:
        linksTable[a].add(b)
        linksTable[b].add(a)
    print 'linksTable =', linksTable


    for start in starts:
        paths = []
        spots = set(others | ends)
        nextP = start[1]







    result = 10

    return result

# @timeIt
def part2(inputData, verbose=False):
    """
    """
    result = 0

    return result



def test():
    return

if __name__=="__main__":
    print(sys.version)

    # go(part1, verbose=False, inputFile='part1_sample1.txt', expected=10)
    # go(part1, verbose=False, inputFile='part1_sample2.txt', expected=19)
    # go(part1, verbose=False, inputFile='part1_sample2.txt', expected=226)
    # go(part1, verbose=False, inputFile='part1_data.txt',    expected=None)

    # go(part2, verbose=False, inputFile='part2_sample1.txt', expected=None)
    # go(part2, verbose=False, inputFile='part2_data.txt',    expected=None)

    test()
