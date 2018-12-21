import sys
import Node
import Parser
from collections import deque

filename = sys.argv[1]
data = open(filename).readlines()
input = ''.join([line.strip() for line in data])
if len(input) > 1000:
    # Input goes deep!
    sys.setrecursionlimit(3000)
else:
    print input

far = 1000
if len(sys.argv) > 2:
    far = int(sys.argv[2])
print 'Far rooms are',far,'away.'

reg = Parser.Parser(input)
check = '^' + str(reg.root) + '$'
if check == input:
    print 'Parsed input correctly.'
else:
    print 'Parse error.'
    sys.exit()

def dump(r):
    """Print out the rooms array."""
    minx = 0
    maxx = 0
    miny = 0
    maxy = 0
    for (x,y) in r:
        if x < minx:
            minx = x
        if x > maxx:
            maxx = x
        if y < miny:
            miny = y
        if y > maxy:
            maxy = y
    out = ''
    for y in range(maxy,miny-1,-1):
        for x in range(minx,maxx+1):
            if (x,y) in r:
                out += '%2d' % r[(x,y)]
            else:
                out += '  '
            if x < maxx:
                out += '|'
        out += '\n'
    print out

rooms = {}  # rooms we've found
plan = deque(['']) # queue of paths to be explored

steps = 0   # steps taken

while plan:
    steps += 1
    path = plan.pop()
    x = path.count('E') - path.count('W')
    y = path.count('N') - path.count('S')
    if (x,y) in rooms:
        # been here already
        olddist = rooms[(x,y)]
        if len(path) >= olddist:
            # got here by a shorter route last time
            continue
    # new room or else new shortest path to this room
    rooms[(x,y)] = len(path)
    for d in 'NSEW':
        newpath = path + d
        # check if newpath is a legal path
        if '' in reg.root.legal(newpath):
            # it is!
            plan.appendleft(path + d)
    if steps % 1000 == 0:
        print 'Step:',steps,'Found rooms:',len(rooms)

#
# Finish up
#

if len(rooms) < 1000:
    dump(rooms)

maxd = 0
farcount = 0
for r in rooms:
    if rooms[r] >= 1000:
        farcount += 1
    if rooms[r] > maxd:
        maxd = rooms[r]

print 'Furthest room:',maxd
print 'Far away rooms:',farcount

