# import fileinput  # TODO(tester ce module)
# import collections

# import os
import sys
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
        inputDataRaw = [x.strip() for x in f.readlines() if x and not x.startswith('#')]
    inputData = inputDataRaw
    return inputData

# @timeIt
def part1(inputData, verbose=False):
    """
    """
    result = 0

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

    go(part1, verbose=False, inputFile='part1_sample1.txt', expected=None)
    # go(part1, verbose=False, inputFile='part1_data.txt',    expected=None)

    # go(part2, verbose=False, inputFile='part2_sample1.txt', expected=None)
    # go(part2, verbose=False, inputFile='part2_data.txt',    expected=None)

    # test()
