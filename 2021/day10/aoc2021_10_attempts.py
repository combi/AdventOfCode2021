# import fileinput  # TODO(tester ce module)
import collections
# import os
# import sys
# import glob
# import re
# import time

def part1(inputData, verbose=False):
    """
    """
    # print 'inputData =', inputData
    # parens   = 0
    # brackets = 0
    # curlys   = 0
    # __test_corrupted = set(
    #     ['{([(<{}[<>[]}>{[]{[(<()>',
    #      '[[<[([]))<([[{}[[()]]]',
    #      '[{[{({}]{}}([{[{{{}}([]',
    #      '[<(<(<(<{}))><([]([]()',
    #      '<{([([[(<>()){}]>(<<{{',])

    # symbols = dict()
    # symbols['('] = ('parens', 1)
    # symbols[')'] = ('parens', -1)
    # symbols['['] = ('brackets', 1)
    # symbols[']'] = ('brackets', -1)
    # symbols['{'] = ('curlys', 1)
    # symbols['}'] = ('curlys', -1)
    # symbols['<'] = ('angles', 1)
    # symbols['>'] = ('angles', -1)

    result = 0
    illegals = collections.Counter()
    for line in inputData:
        chunks = {')': 0 , ']': 0 , '}': 0 , '>': 0}

        # count = 0
        print '\n'
        print 'line =', line
        illegal = None
        illegalScore = 0

        for symbol in line:
            if symbol == '(':
                chunks[')'] += 1
            elif symbol == ')':
                chunks[')'] -= 1
                if chunks[')'] < 0:
                    print 'Diiing )'
                    illegalScore = illegalPoints[symbol]
                    break

            if symbol == '[':
                chunks[']'] += 1
            elif symbol == ']':
                chunks[']'] -= 1
                if chunks[']'] < 0:
                    print 'Diiing ]'
                    illegalScore = illegalPoints[symbol]
                    break

            if symbol == '{':
                chunks['}'] += 1
            elif symbol == '}':
                chunks['}'] -= 1
                if chunks['}'] < 0:
                    print 'Diiing }'
                    # result += illegalPoints[symbol]
                    illegalScore = illegalPoints[symbol]
                    break

            if symbol == '<':
                chunks['>'] += 1
            elif symbol == '>':
                chunks['>'] -= 1
                if chunks['>'] < 0:
                    print 'Diiing >'
                    # result += illegalPoints[symbol]
                    illegalScore = illegalPoints[symbol]
                    break
        print 'illegalScore =', illegalScore
        result += illegalScore

    return result
