# import fileinput  # TODO(tester ce module)
import collections
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


def getData(inputFile):
    with open(inputFile, 'r') as f:
        inputData = [x for x in f.readlines() if x and not x.startswith('#')]
        return inputData


@timeIt
def part1(inputData):
    """
    """
    result = 0
    counts = collections.defaultdict(int)
    numEntries = len(inputData)
    numHalf = numEntries/2

    for line in inputData:
        for i, b in enumerate(line.strip()):
            counts[i]+=int(b)

    gammaRate   = '0b'
    epsilonRate = '0b'

    for _, numBits in sorted(counts.items()):
        if numBits>=numHalf:
            gammaBit   = '1'
            epsilonBit = '0'
        else:
            gammaBit   = '0'
            epsilonBit = '1'
        gammaRate   += gammaBit
        epsilonRate += epsilonBit


    print 'gammaRate =', gammaRate
    print 'epsilonRate =', epsilonRate

    gammaRate   = int(gammaRate, 2)
    epsilonRate = int(epsilonRate, 2)
    result = gammaRate*epsilonRate
    return result

@timeIt
def part2(inputData, verbose=False):
    """
    """
    result = 0

    def reducePool(pool, bitMask, oxyMode=True, verbose=False):
        """ returns a bitMask"""

        bitPos = len(bitMask)
        poolSize = len(pool)
        half     = poolSize/2.0
        if verbose:
            print 'poolSize =', poolSize
            print 'half     =', half, type(half)

        accum = 0
        for line in pool:
            accum+=int(line[bitPos])

        if verbose: print 'accum =', accum

        if accum==half:
            if oxyMode:
                bitMask += '1'
            else:
                bitMask += '0'
        elif accum>half:
            if oxyMode:
                bitMask += '1'
            else:
                bitMask += '0'
        else:
            if oxyMode:
                bitMask += '0'
            else:
                bitMask += '1'

        toDiscard = set()
        for line in pool:
            if not line.startswith(bitMask):
                toDiscard.add(line)
        pool.difference_update(toDiscard)

        return bitMask


    oxyMask = ''
    co2Mask = ''

    data = [l.strip() for l in inputData]
    oxyPool = set(data)
    co2Pool = set(data)

    safety = 5000
    while len(oxyPool) > 1:
        safety -=1
        if safety < 0:
            'safety!!!!!'
            break
        oxyMask = reducePool(oxyPool, oxyMask, oxyMode=True)

    oxyRate = int(oxyPool.pop(), 2)
    print 'oxyRate =', oxyRate

    print

    safety = 5000
    while len(co2Pool) > 1:
        safety -=1
        if safety < 0:
            'safety!!!!!'
            break
        co2Mask = reducePool(co2Pool, co2Mask, oxyMode=False)

    co2Rate = int(co2Pool.pop(), 2)
    print 'co2Rate =', co2Rate

    result = oxyRate*co2Rate

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
        expectedResult = 198
        for inputFile in part1_tests:
            print inputFile
            inputData = getData(inputFile)
            result = part1(inputData)
            print 'result =', result, result == expectedResult
            print

    if part1Final:
        expectedResult = 2595824
        print 'PART 1 FINAL ------------------------------------'
        for inputFile in part1_inputs:
            print inputFile
            inputData = getData(inputFile)
            result = part1(inputData)
            print 'result =', result, result == expectedResult
            print


    if part2Test:
        expectedResult = 230
        print 'PART 2 TESTS ------------------------------------'
        for inputFile in part2_tests:
            print inputFile
            inputData = getData(inputFile)
            result = part2(inputData, verbose=verbose)
            print 'result =', result, result == expectedResult
            print

    if part2Final:
        print 'PART 2 FINAL ------------------------------------'
        expectedResult = None
        for inputFile in part2_inputs:
            print inputFile
            inputData = getData(inputFile)
            result = part2(inputData, verbose=verbose)  # Ma version
            print 'result =', result, result == expectedResult
            print

def test():
    # print int('0b0100011001111100011000101100000101011010010101000011110001110100101010001111110111101100100110010110111000001111011001000001000100001001100110101001110010001001111111001010010010100000111001101110100110100011100000100011101000111011000010100001010010000101010010111110101001001100001100011010110011011001111001110111010001000111011011100100110110100110111101010001011100101101010001110000011100110000100010011100001000100101110101010110001000010100010111100010011100001011101110110000010111111010000010101011001010010010010001100000111011100010110000011100101010001101111011010110110001000111101111111011011101000101111000111111000010101001001001001000001111101001011001111111010111000010111001010110110111011011000011111010111010110010011001100010100011000111011011100100100001100101111011010100011010001110010011000000000010001111111011000101100011101111001101010111010011010101000110100000010110110111101000010111101100100001101011000000111011001011100101111100100011101100010011001101011100011110', 2)

    b1 = '0b10011'
    b2 = '0b10110'
    print 'b1 =', b1
    print 'b2 =', b2
    b1 = int(b1, 2)
    b2 = int(b2, 2)
    r = b1 & b2
    r=bin(r)
    print 'r  =', r

if __name__=="__main__":
    print(sys.version)
    gogo(verbose=False, part1Test=False, part1Final=False, part2Test=True, part2Final=True)
    # test()

