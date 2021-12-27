import collections
import os
import sys
import glob
import re
import time

# test

def gogo(verbose=False):
    location     = os.path.dirname(__file__)
    current      = os.path.basename(__file__).split('.')[0]
    part1_inputs = glob.glob('%s/%s_part1_data.txt' %(location, current))
    part1_tests  = glob.glob('%s/%s_part1_sample*.txt' %(location, current))
    part2_inputs = glob.glob('%s/%s_part2_data.txt' %(location, current))
    part2_tests  = glob.glob('%s/%s_part2_sample*.txt' %(location, current))

    # print 'PART 1 TESTS ------------------------------------'
    # for inputFile in part1_tests:
    #     with open(inputFile, 'r') as f:
    #         inputData = f.readlines()
    #         print 'test   =', inputFile
    #         result = part1(inputData)
    #         print 'result =', result
    #         print

    # print 'PART 1 FINAL ------------------------------------'
    # for inputFile in part1_inputs:
    #     with open(inputFile, 'r') as f:
    #         inputData = f.readlines()
    #         print 'real   =', inputFile
    #         result = part1(inputData)
    #         print 'result =', result
    #         print

    # part2_tests  = ['%s/test.txt' %location]
    # print 'PART 2 TESTS ------------------------------------'
    # for inputFile in part2_tests:
    #     with open(inputFile, 'r') as f:
    #         inputData = f.readlines()
    #         print 'sampleData = ', inputFile
    #         # result = part2(inputData, verbose=verbose)
    #         result = part2_NEW(inputData, verbose=verbose)
    #         print 'result     = ', result
    #         print

    print 'PART 2 FINAL ------------------------------------'
    for inputFile in part2_inputs:
        with open(inputFile, 'r') as f:
            inputData = f.readlines()
            print 'real   =', inputFile
            result = part2(inputData)
            # result = part2_NEW(inputData)
            print 'result =', result
            print

def volume(cuboid, verbose=False):
    if not cuboid:
        return None
    xmin, xmax, ymin, ymax, zmin, zmax = cuboid
    x = xmax - xmin
    y = ymax - ymin
    z = zmax - zmin
    volume = (x+1) * (y+1) * (z+1)
    if verbose:
        print 'cuboid =', cuboid
        print 'volume =', volume
    return volume

def intersect(cuboid1, cuboid2, verbose=False):
    xMin_1, xMax_1, yMin_1, yMax_1, zMin_1, zMax_1 = cuboid1
    xMin_2, xMax_2, yMin_2, yMax_2, zMin_2, zMax_2 = cuboid2

    xMin_r = max(xMin_1,   xMin_2)
    yMin_r = max(yMin_1,   yMin_2)
    zMin_r = max(zMin_1,   zMin_2)

    xMax_r = min(xMax_1,   xMax_2)
    yMax_r = min(yMax_1,   yMax_2)
    zMax_r = min(zMax_1,   zMax_2)

    range_x = range(xMin_r, xMax_r+1)
    range_y = range(yMin_r, yMax_r+1)
    range_z = range(zMin_r, zMax_r+1)

    # if verbose:
    #     print 'range_x =', range_x
    #     print 'range_y =', range_y
    #     print 'range_z =', range_z

    result = (range_x[0], range_x[-1], range_y[0], range_y[-1], range_z[0], range_z[-1]) if all([range_x, range_y, range_z]) else None
    return result

def split(cuboid1, cuboid2, verbose=False):
    """ Cette version nme fonctionne que si cuboid2 est contenu (ou egal) dans cuboid1
    """
    if verbose:
        print 'cuboid1 =', cuboid1
        print 'cuboid2 =', cuboid2

    result = []
    xMin_1, xMax_1, yMin_1, yMax_1, zMin_1, zMax_1 = cuboid1
    xMin_2, xMax_2, yMin_2, yMax_2, zMin_2, zMax_2 = cuboid2

    xa = range(xMin_1, xMin_2)
    xb = range(xMin_2, xMax_2+1)
    xc = range(xMax_2+1, xMax_1+1)

    ya = range(yMin_1, yMin_2)
    yb = range(yMin_2, yMax_2+1)
    yc = range(yMax_2+1, yMax_1+1)

    za = range(zMin_1, zMin_2)
    zb = range(zMin_2, zMax_2+1)
    zc = range(zMax_2+1, zMax_1+1)

    if verbose:
        print 'xa =', xa
        print 'xb =', xb
        print 'xc =', xc
        print 'ya =', ya
        print 'yb =', yb
        print 'yc =', yc
        print 'za =', za
        print 'zb =', zb
        print 'zc =', zc


    xRanges = [r for r in (xa, xb, xc) if r]
    yRanges = [r for r in (ya, yb, yc) if r]
    zRanges = [r for r in (za, zb, zc) if r]

    splitCuboids = set()
    for x in xRanges:
        for y in yRanges:
            for z in zRanges:
                splitCuboid = (x[0], x[-1], y[0], y[-1], z[0], z[-1])
                splitCuboids.add(splitCuboid)

    if verbose:
        print 'splitCuboids:'
        for sc in splitCuboids:
            print sc

        print len(splitCuboids), 'cuboids'

    result = splitCuboids
    return result

def part1(inputData):
    """ Cette version je l'ai copiee de https://www.twitch.tv/larryny/video/1240221664 !
        J'etais curieux de voir si ca marchait vraiment, et ensuite j'ai ete pique au jeu ^^
    """
    result = 0
    C = collections.defaultdict(bool)
    for line in inputData:
        val = line.startswith('on')
        numbers = list(int(x) for x in re.findall(r'(-?\d+)', line))
        x0, x1, y0, y1, z0, z1 = numbers

        for x in range(max(x0, -50), min(x1+1, 50+1)):
            for y in range(max(y0, -50), min(y1+1, 50+1)):
                for z in range(max(z0, -50), min(z1+1, 50+1)):
                    C[(x,y,z)] = val

    cellsOn = 0
    for cell, val in C.items():
        if val:
            cellsOn += 1

    result = cellsOn
    return result

def part2(inputData, verbose=False):
    """ Cette version je l'ai elaboree tout seul par contre, a 100%
        C'est rigolo de voir apres coup que plein d'autres participants ont eu la mem approche.
    """
    startTime = time.time()

    result = 0

    cuboids = set()

    for line in inputData:
        val = line.startswith('on')
        numbers = list(int(x) for x in re.findall(r'(-?\d+)', line))
        x0, x1, y0, y1, z0, z1 = numbers
        currentCuboid = (x0, x1, y0, y1, z0, z1)
        if verbose:
            print
            print 'currentCuboid = %s (%s)' %(currentCuboid, val)
            print 'Will test against %s cuboids' %len(cuboids)
        toAdd = set()
        toDel = set()
        if val:
            toAdd.add(currentCuboid)

        for cuboid in cuboids:
            if verbose:
                print
                print '   Testing against cuboid: %s' %str(cuboid)
            intersection = intersect(currentCuboid, cuboid, verbose=False)
            # intersects = any(intersection)
            if verbose:
                print '   Intersects at %s' %str(intersection)
            if intersection:
                toDel.add(cuboid)
                splittedCuboids = split(cuboid, intersection, verbose=False)
                toAdd.update([c for c in splittedCuboids if not intersect(currentCuboid, c)])
                if verbose:
                    print '   Splitted into %s new cuboids' %len(splittedCuboids)
                # print 'toAdd =', toAdd
        cuboids.update(toAdd)
        cuboids.difference_update(toDel)


    # if verbose: print 'cuboids =', cuboids

    print '%s resulting cuboids' %len(cuboids)
    for cuboid in cuboids:
        result+=volume(cuboid)

    elapsed = time.time() - startTime
    print 'elapsed =', elapsed
    return result




class Instruction(object):
    def __init__(self, x0, x1, y0, y1, z0, z1, val):
        self.x0    = x0
        self.x1    = x1
        self.y0    = y0
        self.y1    = y1
        self.z0    = z0
        self.z1    = z1
        self.val = val

    def __repr__(self):
        valStr = 'On' if self.val else 'Off'
        str__ = '%s (%s, %s, %s, %s, %s, %s)' %(valStr, self.x0, self.x1, self.y0, self.y1, self.z0, self.z1)
        return(str__)

def part2_NEW(inputData, verbose=False):
    """
        Je tente d'implementer la meme solution (Coordinate compression) que ce gars:
        https://www.youtube.com/watch?v=YKpViLcTp64&t=901s
        mais je bute sur des limites memoires a chaque tentative.

    """
    result = 0
    instructions = []

    # X = []
    # Y = []
    # Z = []

    X = set()
    Y = set()
    Z = set()

    # print 'inputData =', inputData
    for line in inputData:
        val = line.startswith('on')
        numbers = list(int(x) for x in re.findall(r'(-?\d+)', line))
        x0, x1, y0, y1, z0, z1 = numbers

        x1+=1
        y1+=1
        z1+=1

        instructions.append(Instruction(x0, x1, y0, y1, z0, z1, val))
        X.update((x0, x1))
        Y.update((y0, y1))
        Z.update((z0, z1))

    # X.sort()
    # Y.sort()
    # Z.sort()

    X = sorted(X)
    Y = sorted(Y)
    Z = sorted(Z)

    print X[0], X[-1]
    print Y[0], Y[-1]
    print Z[0], Z[-1]

    Nx = len(X)
    Ny = len(Y)
    Nz = len(Z)

    print 'Nx =', Nx
    print 'Ny =', Ny
    print 'Nz =', Nz
    # print Nx*Ny*Nz

    return   # DEBUGONLY

    grid = collections.defaultdict(bool)

    cuboids = set()

    # for inst in instructions:
    for inst in instructions[0:30]:
        x0 = X.index(inst.x0)
        x1 = X.index(inst.x1)
        y0 = Y.index(inst.y0)
        y1 = Y.index(inst.y1)
        z0 = Z.index(inst.z0)
        z1 = Z.index(inst.z1)
        val = inst.val
        # print
        # print 'inst =', inst
        # print 'x0 =', x0
        # print 'x1 =', x1
        # print 'y0 =', y0
        # print 'y1 =', y1
        # print 'z0 =', z0
        # print 'z1 =', z1

        for x in range(x0, x1+1):
            # print 'x =', x
            for y in range(y0, y1+1):
                for z in range(z0, z1+1):
                    # grid[(x,y,z)] = val
                    cuboid = (x, x+1, y, y+1, z, z+1)
                    if val:
                        cuboids.add(cuboid)
                    else:
                        cuboids.discard(cuboid)

    print '%s resulting cuboids' %len(cuboids)

    return   # DEBUGONLY

    # print 'Nx =', Nx  # X Y et Z sont supposes avoir la meme taille
    for x in range(Nx-1):
        for y in range(Ny-1):
            for z in range(Nz-1):
                result += grid[(x,y,z)] * (X[x+1]-X[x])  * (Y[y+1]-Y[y]) * (Z[z+1]-Z[z])

    return result

def test():

    # -----------------------------
    # a = (10, 11, 10, 11, 10, 11)
    # b = (11, 12, 11, 12, 11, 12)
    # iab = intersect(a, b)
    # print 'iab =', iab, 'volume=', volume(iab)

    # a = (10, 11, 10, 11, 10, 11)
    # b = (10, 12, 10, 12, 10, 12)
    # iab = intersect(a, b)
    # print 'iab =', iab, 'volume=', volume(iab)

    # a = (10, 12, 10, 12, 10, 10)
    # b = (11, 11, 11, 11, 0, 100)
    # iab = intersect(a, b)
    # print 'iab =', iab, 'volume=', volume(iab)

    # # -----------------------------
    # a = (10, 13, 10, 13, 10, 13)
    # # b = (10, 13, 10, 13, 10, 13)
    # # b = (5, 15, 5, 15, 5, 15)
    # b = (10, 13, 10, 13, 10, 13)
    # split(a, b, verbose=True)
    # # -----------------------------

    cubs = []
    r = [15,16,17,18]
    r0 = r[0]
    r1 = r[-1]+1
    print 'r1 =', r1
    for i in range(r0, r1-1):
        print i
        cubs.append((i, i+1))
    print 'cubs =', cubs

if __name__=="__main__":
    print(sys.version)
    # print(sys.path)
    gogo(verbose=True)
    # cuboid = (10,12,10,12,10,12)
    # vol = volume(cuboid, verbose=True)

    # test()
