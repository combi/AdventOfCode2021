# import fileinput  # TODO(tester ce module)
import collections
import os
import sys
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


class Cuboid(object):
    def __init__(self, x0, x1, y0, y1, z0, z1, val=True):
        self.x0  = x0
        self.x1  = x1
        self.y0  = y0
        self.y1  = y1
        self.z0  = z0
        self.z1  = z1
        self.val = val

    @property
    def coords(self):
        return (self.x0, self.x1, self.y0, self.y1, self.z0, self.z1)

    @property
    def volume(self):
        return (self.x1 - self.x0+1) * (self.y1 - self.y0+1) * (self.z1 - self.z0+1)

    @property
    def volumeSigned(self):
        return self.volume if self.val else -self.volume

    @property
    def empty(self):
        return volume<=0

    @property
    def isValid(self):
        return self.x0<=self.x1 and self.y0<=self.y1 and self.z0<=self.z1

    def __hash__(self):
        return hash((self.x0, self.x1, self.y0, self.y1, self.z0, self.z1, self.val))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.coords == other.coords and self.val == other.val

    def __repr__(self):
        valStr = 'On' if self.val else 'Off'
        str__ = '%s (%s, %s, %s, %s, %s, %s)' %(valStr, self.x0, self.x1, self.y0, self.y1, self.z0, self.z1)
        return(str__)



def cuboidFromInstruction(instruction):
    cuboidDatas = re.search(r'(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)', instruction)
    val = cuboidDatas.group(1) == 'on'
    x0, x1, y0, y1, z0, z1 = [int(_) for _ in cuboidDatas.groups()[1:]]
    cuboid = Cuboid(x0, x1, y0, y1, z0, z1, val)
    return cuboid

def volume(cuboid, verbose=False):
    if not cuboid:
        return None
    xmin, xmax, ymin, ymax, zmin, zmax = cuboid.coords

    x = xmax - xmin
    y = ymax - ymin
    z = zmax - zmin
    volume = (x+1) * (y+1) * (z+1)

    if verbose:
        print 'cuboid =', cuboid
        print 'volume =', volume
    return volume


def intersect(c1, c2, negateFromSecond=False, verbose=False):
    if verbose:
        print
        print 'cuboid1 =', c1
        print 'cuboid2 =', c2

    if (c1.x0 > c2.x1) or (c2.x0 > c1.x1):
        return
    if (c1.y0 > c2.y1) or (c2.y0 > c1.y1):
        return
    if (c1.z0 > c2.z1) or (c2.z0 > c1.z1):
        return

    x0 = max(c1.x0,   c2.x0)
    y0 = max(c1.y0,   c2.y0)
    z0 = max(c1.z0,   c2.z0)

    x1 = min(c1.x1,   c2.x1)
    y1 = min(c1.y1,   c2.y1)
    z1 = min(c1.z1,   c2.z1)

    result = Cuboid(x0, x1, y0, y1, z0, z1)

    if negateFromSecond:
        result.val = not c2.val

    return result


def split(c1, c2, verbose=False):
    """ Cette version nme fonctionne que si cuboid2 est contenu (ou egal) dans c1
    """
    if verbose:
        print
        print 'split_NEW'
        print 'c1 =', c1, 'isValid', c1.isValid, 'vol=', c1.volume
        print 'c2 =', c2, 'isValid', c2.isValid, 'vol=', c2.volume

    sub1 = Cuboid(c1.x0, c2.x0-1, c1.y0, c1.y1, c1.z0, c1.z1)
    sub2 = Cuboid(c2.x0, c2.x1, c1.y0, c1.y1, c1.z0, c2.z0-1)
    sub3 = Cuboid(c2.x0, c2.x1, c1.y0, c2.y0-1, c2.z0, c2.z1)
    sub4 = Cuboid(c2.x0, c2.x1, c2.y1+1, c1.y1, c2.z0, c2.z1)
    sub5 = Cuboid(c2.x0, c2.x1, c1.y0, c1.y1, c2.z1+1, c1.z1)
    sub6 = Cuboid(c2.x1+1, c1.x1, c1.y0, c1.y1, c1.z0, c1.z1)
    if verbose:
        print
        print 'sub1 =', sub1, 'isValid', sub1.isValid, 'vol=', sub1.volume
        print 'sub2 =', sub2, 'isValid', sub2.isValid, 'vol=', sub2.volume
        print 'sub3 =', sub3, 'isValid', sub3.isValid, 'vol=', sub3.volume
        print 'sub4 =', sub4, 'isValid', sub4.isValid, 'vol=', sub4.volume
        print 'sub5 =', sub5, 'isValid', sub5.isValid, 'vol=', sub5.volume
        print 'sub6 =', sub6, 'isValid', sub6.isValid, 'vol=', sub6.volume

    result = [c for c in (sub1, sub2, sub3, sub4, sub5, sub6) if c.isValid]
    if verbose:
        print 'result :'
        for sc in result:
            print sc

        resultVol = sum([c.volume for c in result])
        print '%d subCuboids for a total volume of %s' %(len(result), resultVol)

    return result

def cuboidsBB(cuboids):
    x0 = min([c.x0 for c in cuboids])
    x1 = max([c.x1 for c in cuboids])
    y0 = min([c.y0 for c in cuboids])
    y1 = max([c.y1 for c in cuboids])
    z0 = min([c.z0 for c in cuboids])
    z1 = max([c.z1 for c in cuboids])

    result = Cuboid(x0, x1, y0, y1, z0, z1)
    # print 'result =', result
    return result

def cuboidsVol(cuboids, verbose=False):
    result = sum([c.volume for c in cuboids])
    if verbose:
        print 'volume =', result
    return result


@timeIt
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
    # print '%s cells' %len(C)
    return result

@timeIt
def part2(inputData, verbose=False):
    """ Cette version je l'ai elaboree tout seul par contre, a 100%
        C'est rigolo de voir apres coup que plein d'autres participants ont eu la meme approche.
        Changements depuis version initiale:
            - On utilise une classe Cuboid.
            - On utilise une nouvelle version de split pour produire moins de subCuboids (j'ai tente de trouver mi meme, mais je suis pas arrive alors j'ai mate sur reddit)

    """
    result = 0

    cuboids = set()

    for instruction in inputData:
        currentCuboid = cuboidFromInstruction(instruction)
        if verbose:
            print
            print 'currentCuboid =', currentCuboid
        toAdd = set()
        toDel = set()
        if currentCuboid.val:
            toAdd.add(currentCuboid)

        for cuboid in cuboids:
            if verbose:
                print
                print '   Testing against cuboid: %s' %cuboid

            intersectionCuboid = intersect(currentCuboid, cuboid, verbose=False)

            if verbose:
                print '   Intersects at %s' %intersectionCuboid
            if intersectionCuboid:
                toDel.add(cuboid)
                splittedCuboids = split(cuboid, intersectionCuboid, verbose=False)
                toAdd.update(splittedCuboids)
                if verbose:
                    print '   Splitted into %s new cuboids' %len(splittedCuboids)
        cuboids.update(toAdd)
        cuboids.difference_update(toDel)


    print '%s resulting cuboids:' %len(cuboids)
    if verbose:
        print '%s resulting cuboids:' %len(cuboids)
        print cuboids

    for cuboid in cuboids:
        result+=cuboid.volume

    return result



@timeIt
def part22(inputData, useNewIntersect=False, verbose=False):
    """ Cette version je l'ai retranscrite depuis ce post:

    https://www.reddit.com/r/adventofcode/comments/rlxhmg/comment/hpizza8/?utm_source=share&utm_medium=web2x&context=3

    No splitting cubes or anything with my approach.
    My strategy was just to use signed volumes and track the intersections.
    Each cell could be in any number of the accumulated cubes so long as the
    final tally of the signs for the cubes containing it was either 0 or 1.
    Basically, when a new "on" comes in, it first finds intersections with
    any existing positive or negative cubes and adds a new cube for the
    intersection with the opposite sign to cancel them out.
    This way, the final tally for all cells within the new cube
    has been zeroed. Then it adds the new cube with a positive sign.
    For "off" lines, we do the same cancellation of everything intersecting
    the cube's space, but then just leave them cancelled.
    Then at the end, we just tally up the signed volumes.
    """
    result = 0

    # cuboids = set()
    cuboids = []

    for instruction in inputData:
        currentCuboid = cuboidFromInstruction(instruction)
        if verbose:
            print
            print 'currentCuboid =', currentCuboid
        # toAdd = set()
        toAdd = []
        if currentCuboid.val:
            # toAdd.add(currentCuboid)
            toAdd.append(currentCuboid)

        for cuboid in cuboids:
            if verbose:
                print
                print '   Testing against cuboid: %s' %cuboid
            intersectionCuboid = intersect(currentCuboid, cuboid, useNew=useNewIntersect, negateFromSecond=True, verbose=False)
            if verbose:
                print '   Intersects at %s' %intersectionCuboid
            if intersectionCuboid:
                # toAdd.add(intersectionCuboid)
                toAdd.append(intersectionCuboid)
        # cuboids.update(toAdd)
        cuboids.extend(toAdd)


    if verbose: print 'cuboids =', cuboids

    print '%s resulting cuboids' %len(cuboids)
    for cuboid in cuboids:
        result+=cuboid.volumeSigned

    return result

# @timeIt
def part23(inputData, verbose=False):
    """ Ici on parcourt a l'envers
        J'essaie de tester cette approche proposee ici:
        https://www.reddit.com/r/adventofcode/comments/rlxhmg/comment/hppx86d/?utm_source=share&utm_medium=web2x&context=3
        https://gist.github.com/robinhouston/2c9dc527d95357c5aa19e33e5368fb01

        Mais ca marche pas encore

    """
    startTime = time.time()

    result = 0

    cuboids = set()

    for instruction in inputData[::-1]:
        if verbose: print 'instruction =', instruction
        # continue
        currentCuboid = cuboidFromInstruction(instruction)
        if verbose:
            print
            # print 'currentCuboid = %s (%s)' %(currentCuboid, val)
            print 'currentCuboid =', currentCuboid
            # print 'Will test against %s cuboids' %len(cuboids)
        if currentCuboid.val:
            volume = currentCuboid.volume

            for cuboid in cuboids:
                if verbose:
                    print
                    print '   Testing against cuboid: %s' %cuboid
                intersectionCuboid = intersect(currentCuboid, cuboid, verbose=False)
                if intersectionCuboid:
                    volume -= intersectionCuboid.volume

        cuboids.add(currentCuboid)

    print '%s resulting cuboids' %len(cuboids)
    # for cuboid in cuboids:
    #     result+=cuboid.volumeSigned
    result = volume
    elapsed = time.time() - startTime
    print 'elapsed =', elapsed
    return result

def part2_CC(inputData, verbose=False):
    """
        Je tente d'implementer la meme solution (Coordinate compression) que ce gars:
        https://www.youtube.com/watch?v=YKpViLcTp64&t=901s
        mais je bute sur des limites memoires a chaque tentative.

    """
    result = 0
    cuboids = []

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

        cuboids.append(Cuboid(x0, x1, y0, y1, z0, z1, val))
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

    final_cuboids = set()

    # for inst in instructions:
    for cuboid in cuboids[0:30]:
        x0 = X.index(cuboid.x0)
        x1 = X.index(cuboid.x1)
        y0 = Y.index(cuboid.y0)
        y1 = Y.index(cuboid.y1)
        z0 = Z.index(cuboid.z0)
        z1 = Z.index(cuboid.z1)
        val = cuboid.val
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
                    grid[(x,y,z)] = val
                    # cuboid_ = Cuboid(x, x+1, y, y+1, z, z+1, val)
                    # if val:
                    #     final_cuboids.add(cuboid_)
                    # else:
                    #     final_cuboids.discard(cuboid_)

    print '%s resulting final_cuboids' %len(final_cuboids)

    return   # DEBUGONLY

    # print 'Nx =', Nx  # X Y et Z sont supposes avoir la meme taille
    for x in range(Nx-1):
        for y in range(Ny-1):
            for z in range(Nz-1):
                result += grid[(x,y,z)] * (X[x+1]-X[x])  * (Y[y+1]-Y[y]) * (Z[z+1]-Z[z])

    return result


def getData(inputFile):
    with open(inputFile, 'r') as f:
        inputData = [x for x in f.readlines() if x and not x.startswith('#')]
        return inputData


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
            print 'test   =', inputFile
            inputData = getData(inputFile)
            result = part1(inputData)
            print 'result =', result
            print

    if part1Final:
        print 'PART 1 FINAL ------------------------------------'
        for inputFile in part1_inputs:
            print 'real   =', inputFile
            inputData = getData(inputFile)
            result = part1(inputData)
            print 'result =', result
            print


    if part2Test:
        expectedResult = 2758514936282235
        # part2_tests  = ['%s/test.txt' %location]
        print 'PART 2 TESTS ------------------------------------'
        for inputFile in part2_tests:
            print 'sampleData = ', inputFile
            inputData = getData(inputFile)
            result = part2(inputData, verbose=verbose)  # Ma version
            print 'result1     = ', result
            print 'result1 =', result, result == expectedResult
            # result2 = part22(inputData, verbose=verbose)  # Ma premiere version
            # print 'result2     = ', result2
            # print 'difference:', result2 - result
            # resultCC = part2_CC(inputData, verbose=verbose)
            # print 'resultCC =', resultCC
            print

    if part2Final:
        print 'PART 2 FINAL ------------------------------------'
        expectedResult = 1261885414840992
        for inputFile in part2_inputs:
            print 'real   =', inputFile
            inputData = getData(inputFile)
            result = part2(inputData, verbose=verbose)  # Ma version
            print 'result1 =', result, result == expectedResult
            # result2 = part22(inputData)  # Une version ou je teste une classe de cuboid qui contient les coords, et la valeur
            # print 'result2 = ', result2
            # print 'difference:', result2 - result
            # resultCC = part2_CC(inputData)
            # print 'resultCC =', resultCC
            # print

def test():
    # 645613097778958
    # 1261885414840992
    2758514936282235
    3095639194231007
    337124257948772

    2758514936282235
    2759684270216175

    # -----------------------------------------------------------------
    # a = Cuboid(10, 11, 10, 11, 10, 11)
    # b = Cuboid(12, 13, 12, 13, 12, 13)
    # iab = intersect(a, b)
    # print 'iab =', iab, 'volume=', volume(iab)

    # a = Cuboid(26, 39, 40, 50, -2, 11)
    # b = Cuboid(-44, 5, -27, 21, -14, 35)
    # iab = intersect(a, b)
    # print 'iab =', iab, 'volume=', volume(iab)

    # a = Cuboid(-43, -33, -45, -28, 7, 25)
    # b = Cuboid(-41, -1, -11, 6, -10, 8)
    # iab = intersect(a, b, verbose=True)
    # print 'iab =', iab, 'volume=', volume(iab)


    # a = (10, 11, 10, 11, 10, 11)
    # b = (10, 12, 10, 12, 10, 12)
    # iab = intersect(a, b)
    # print 'iab =', iab, 'volume=', volume(iab)

    # a = (10, 12, 10, 12, 10, 10)
    # b = (11, 11, 11, 11, 0, 100)
    # iab = intersect(a, b)
    # print 'iab =', iab, 'volume=', volume(iab)

    # -----------------------------------------------------------------
    # # a = cuboidFromInstruction('on x=0..49,y=-19..25,z=-12..38')
    # # b = cuboidFromInstruction('on x=-31..14,y=-46..5,z=-43..9')
    # # i = intersect_NEW(a, b)

    # # a = cuboidFromInstruction('on x=0..49,y=-19..25,z=-12..38')
    # # b = cuboidFromInstruction('on x=-31..14,y=-46..5,z=-43..9')
    # # i = intersect_NEW(a, b)
    # a = Cuboid(0, 49, 0, 25, -12, 38)
    # i = Cuboid(0, 14, 0, 5, -12, 9)
    # print 'a =', a
    # # print 'b =', b
    # print 'i =', i

    # # split__0(a, b, verbose=True)
    # # print '====================='
    # v1 = split(a, i, rejectB=False, verbose=True)
    # v1 = set([x for x in v1 if not x.coords == i.coords])
    # v1Vol = cuboidsVol(v1); print 'v1Vol =', v1Vol
    # print '====================='
    # v2 = split(a, i, rejectB=True, verbose=True)
    # v2Vol = cuboidsVol(v2); print 'v2Vol =', v2Vol
    # print '====================='
    # v3 = split_NEW(a, i, verbose=True)
    # v3Vol = cuboidsVol(v3); print 'v3Vol =', v3Vol
    # print '====================='
    # print 'v1 =', v1
    # print 'v2 =', v2
    # print 'v1 == v2 =', v1 == v2
    # print 'v1Vol == v2Vol =', v1Vol == v2Vol
    # print 'v3 =', v3
    # print 'v1 == v3 =', v1 == v3
    # print 'v1Vol == v3Vol =', v1Vol == v3Vol

    # bb1 = cuboidsBB(v1); print 'bb1 =', bb1
    # bb2 = cuboidsBB(v2); print 'bb2 =', bb2
    # bb3 = cuboidsBB(v3); print 'bb3 =', bb3


    print '====================='

    a = Cuboid(4, 10, 2, 9, 0, 0)
    b = Cuboid(5, 6, 5, 6, 0, 0)
    s = split(a, b, verbose=True)

    abBB = cuboidsBB([a,b])
    sBB  = cuboidsBB(s)
    print 'abBB =', abBB
    print 'sBB =', sBB

    print '====================='
    # -----------------------------------------------------------------

    # a = Cuboid(10, 13, 10, 13, 10, 13, True)
    # # b = (10, 13, 10, 13, 10, 13)
    # # b = Cuboid(11, 12, 11, 12, 11, 12, True)
    # b = Cuboid(10, 13, 10, 13, 10, 13, False)
    # print a==b

    # -----------------------------------------------------------------

    # cubs = []
    # r = [15,16,17,18]
    # r0 = r[0]
    # r1 = r[-1]+1
    # print 'r1 =', r1
    # for i in range(r0, r1-1):
    #     print i
    #     cubs.append((i, i+1))
    # print 'cubs =', cubs

    # -----------------------------------------------------------------

    # cuboids = []
    # cuboids.append(Cuboid(0, 1, 0, 1, 0, 1, True))
    # cuboids.append(Cuboid(0, 2, 0, 2, 0, 2, True))
    # cuboids.append(Cuboid(2, 2, 0, 2, 0, 0, True))
    # for cuboid in cuboids:
    #     print cuboid
    #     print cuboid.volume
    #     print cuboid.volumeSigned
    #     print cuboid.val

    # -----------------------------------------------------------------
    # inputFile = '/home/combi/DEV/PYTHON/AdventOfCode/aoc2021_22_part2_data.txt'
    # inputFile = '/home/combi/DEV/PYTHON/AdventOfCode/test.txt'
    # inputData = getData(inputFile)

    # part22Test(inputData)

    # -----------------------------------------------------------------


if __name__=="__main__":
    print(sys.version)
    # print(sys.path)
    # test()
    # gogo(verbose=False, part2Test=True)
    # gogo(verbose=True, part2Test=True)
    # gogo(verbose=False, part2Final=True)

    gogo(verbose=False, part1Final=False, part2Test=True, part2Final=True)
