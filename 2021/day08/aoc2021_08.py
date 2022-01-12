# import fileinput  # TODO(tester ce module)
import collections
import os
import sys
import glob
# import re
import time

EXPECTED_TEST1  = 26
EXPECTED_FINAL1 = 530
EXPECTED_TEST2  = 61229
EXPECTED_FINAL2 = 1051087

'''
 _
| |
|_|  6 segments  <<

  |
  |  2 segments  <<------------------
 _
 _|
|_   5 segments  <<
 _
 _|
 _|  5 segments  <<

|_|
  |  4 segments  <<------------------
 _
|_
 _|  5 segments  <<
 _
|_
|_|  6 segments  <<
 _
  |
  |  3 segments  <<------------------
 _
|_|
|_|  7 segments  <<------------------
 _
|_|
 _|  6 segments  <<

=========================================================

  |
  |  2 segments  <<------------------

|_|
  |  4 segments  <<------------------
 _
  |
  |  3 segments  <<------------------
 _
|_|
|_|  7 segments  <<------------------


=========================================================

   6          5
segments   segments
 _            _
| |           _|
|_|          |_
 _            _
|_            _|
|_|           _|
 _            _
|_|          |_
 _|           _|



'''

GOOD_MAP = dict()
GOOD_MAP[0] = set('abcefg')
GOOD_MAP[1] = set('cf')
GOOD_MAP[2] = set('acdeg')
GOOD_MAP[3] = set('acdfg')
GOOD_MAP[4] = set('bcdf')
GOOD_MAP[5] = set('abdfg')
GOOD_MAP[5] = set('abdfg')
GOOD_MAP[6] = set('abdefg')
GOOD_MAP[7] = set('acf')
GOOD_MAP[8] = set('abcdefg')
GOOD_MAP[9] = set('abcdfg')


TRANSLATE_DICT = dict()

numSegmentsToNumber = {
    2:1,  # 2 segments > it is the number 1
    3:7,  # 3 segments > it is the number 7
    4:4,  # 4 segments > it is the number 4
    7:8}  # 7 segments > it is the number 8

def gogo(verbose=False, part1Test=False, part1Final=False, part2Test=False, part2Final=False):
    location     = os.path.dirname(__file__)
    current      = os.path.basename(__file__).split('.')[0]
    part1_inputs = sorted(glob.glob('%s/%s_part1_data.txt' %(location, current)))
    part1_tests  = sorted(glob.glob('%s/%s_part1_sample*.txt' %(location, current)))
    part2_inputs = sorted(glob.glob('%s/%s_part2_data.txt' %(location, current)))
    part2_tests  = sorted(glob.glob('%s/%s_part2_sample*.txt' %(location, current)))

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
    inputDataRaw = []
    with open(inputFile, 'r') as f:
        for l in f.readlines():
            if l.startswith('#'):
                continue
            i, o = l.split('|')
            i = i.strip().split(' ')
            o = o.strip().split(' ')
            inputDataRaw.append((i, o))

    inputData = inputDataRaw
    # for x in inputData:
    #     print x
    return inputData


@timeIt
def part1(inputData, verbose=False):
    """
    """
    result = 0
    for I,O, in inputData:
        if verbose: print I, O
        for o in O:
            numSegments = len(o)
            is1478 = numSegments in numSegmentsToNumber
            if verbose: print '  o =', o, is1478
            if is1478:
                result += 1
    return result

@timeIt
def part2(inputData, verbose=False):
    """
    """
    result = 0

    for I,O in inputData:
        CURRENT_MAP = dict()

        byNumSegs = collections.defaultdict(set)
        for i in I:
            numSegments = len(i)
            byNumSegs[numSegments].add(i)

            foundNumber = numSegmentsToNumber.get(numSegments)
            if foundNumber:
                CURRENT_MAP[foundNumber] = set(i)

        a  = CURRENT_MAP[7] - CURRENT_MAP[1]
        bd = CURRENT_MAP[4] - CURRENT_MAP[1]
        eg = CURRENT_MAP[8] - (CURRENT_MAP[4] | a)
        for s in byNumSegs[5]:
            s_ = set(s)
            if CURRENT_MAP[7].issubset(s_):
                CURRENT_MAP[3]=s_
                break
        CURRENT_MAP[9] = CURRENT_MAP[3] | bd
        be = CURRENT_MAP[8] - CURRENT_MAP[3]
        e = CURRENT_MAP[8] - CURRENT_MAP[9]
        g = eg - e
        CURRENT_MAP[0] = CURRENT_MAP[1] | be | a | g

        for s in byNumSegs[5]:
            s_ = set(s)
            if eg.issubset(s_):
                CURRENT_MAP[2]=s_
                break

        for s in byNumSegs[5]:
            s_ = set(s)
            if s_ != CURRENT_MAP[2] and s_ != CURRENT_MAP[3]:
                CURRENT_MAP[5]=s_
                break

        CURRENT_MAP[6] = CURRENT_MAP[5] | e


        assert(CURRENT_MAP[3])
        assert(CURRENT_MAP[9])
        assert(CURRENT_MAP[0])
        assert(CURRENT_MAP[2])
        assert(CURRENT_MAP[5])
        assert(CURRENT_MAP[6])

        current4DigitNum = ''
        for o in O:
            o_ = set(o)
            for number, segments in CURRENT_MAP.items():
                if o_ == segments:
                    current4DigitNum += str(number)
                    break

        number = int(current4DigitNum)

        result += number
    return result

'''
aaaa
b  c
b  c
dddd
e  f
e  f
gggg

-------------------------------

  |
  |
 _
 _|
 _|

|_|
  |
 _
  |
  |
 _
|_|
|_|
 _
|_|
 _|

-------------------------------
...      ...
|_. bd   ... eg
...      |_.

-------------------------------
   5           6
segments    segments
   _           _
   _|         | |
  |_          |_|
   _           _
   _|         |_
   _|         |_|
   _           _
  |_          |_|
   _|          _|

'''




if __name__=="__main__":
    print(sys.version)
    gogo(verbose=False, part1Test=True, part1Final=True, part2Test=True, part2Final=True)
