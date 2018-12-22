import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

data = [x.strip() for x in open(args.filename).readlines()]

depth = int(data[0].split()[1])
targetl = [int(x) for x in data[1].split()[1].split(',')]
target = (targetl[0],targetl[1])

print 'depth:',depth
print 'target:',target

elevels = {}
gindexes = {}

ROCKY = '.'
WET = '='
NARROW = '|'

TORCH = 'T'
CLIMB = 'C'
NONE = 'N'
tools = [TORCH,CLIMB,NONE]

types = ['.','=','|']

def neighbors(x,y):
    n = [(x+1,y),(x,y+1)]
    if x > 0:
        n.append((x-1,y))
    if y > 0:
        n.append((x,y-1))
    return n


def elevel(r):
    if r not in elevels:
        elevels[r] = (gindex(r) + depth) % 20183
    return elevels[r]

def gindex(r):
    if r not in gindexes:
        x,y = r
        if (x,y) == (0,0) or (x,y) == target:
            g = 0
        elif y == 0:
            g =  x * 16807
        elif x == 0:
            g = y * 48271
        else:
            g = elevel( (x-1,y) ) * elevel( (x,y-1) )
        gindexes[r] = g
    return gindexes[r]

def rtype(r):
    return types[elevel(r) % 3]

risks = {ROCKY:0,WET:1,NARROW:2}
risk = 0
for y in range(target[1]+1):
    row = ''
    for x in range(target[0]+1):
        if (x,y) == (0,0):
            row += 'M'
        elif (x,y) == target:
            row += '$'
        else:
            t = rtype( (x,y) )
            risk += risks[t]
            row += t
#    print row
print 'Total risk:',risk

reachable = [set([(0,0,TORCH)])]
allreachable = reachable[0]

disallowed = {
    ROCKY : NONE,
    WET : TORCH,
    NARROW : CLIMB
}

switch = {
    (ROCKY,TORCH) : CLIMB,
    (ROCKY,CLIMB) : TORCH,
    (WET,CLIMB) : NONE,
    (WET,NONE) : CLIMB,
    (NARROW,TORCH) : NONE,
    (NARROW,NONE) : TORCH
}

def dump():
    for t in range(len(reachable)):
        print '%2d' % t, reachable[t]

def shortdump():
    for t in range(len(reachable)):
        print len(reachable[t]),
    print

goal = (target[0],target[1],TORCH)
print 'Goal:',goal
print 'Time:',0
#dump()
time = 0
while True:
    time += 1
    reachable.append(set())
    # try to move with current gear
    for (x,y,gear) in reachable[time-1]:
        for (nx,ny) in neighbors(x,y):
            if gear == disallowed[rtype( (nx,ny) )]:
                continue
            if (nx,ny,gear) not in allreachable:
                reachable[time].add( (nx,ny,gear) )
    if time >= 7:
        # try to switch gear
        for (x,y,gear) in reachable[time-7]:
            ngear = switch[ ( rtype( (x,y) ), gear ) ]
            if (x,y,ngear) not in allreachable:
                reachable[time].add( (x,y,ngear) )

    allreachable = allreachable.union(reachable[time])
    if goal in allreachable:
        print 'Done!'
        break
    if time % 100 == 0:
        print 'Time:',time
#    print allreachable
#    raw_input()

print 'Finish time:',time

