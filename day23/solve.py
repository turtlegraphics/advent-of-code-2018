"""
For Part 2, run the program with increasing arguments until you get it.
For my input, using 950 as the cut point was enough to find the winner.
"""
import sys

filename = sys.argv[1]
data = open(filename).readlines()

bots = []
for line in data:
    p,r = line.strip().split(' ')
    p = p.strip(' ,')[5:-1]
    r = int(r[2:])
    (x,y,z) = [int(c) for c in p.split(',')]
    bots.append((r,x,y,z))

def dist(b1,b2):
    (r1,x1,y1,z1) = b1
    (r2,x2,y2,z2) = b2
    return abs(x1-x2) + abs(y1-y2) + abs(z1-z2)

def norm(s):
    (r,x,y,z) = s
    return abs(x)+abs(y)+abs(z)

# part 1
bots.sort(reverse=True)
count = 0
maxr = bots[0][0]

for bot in bots:
    if dist(bot, bots[0]) <= maxr:
        count += 1
print 'In range of max radius bot:',count


# part 2
def top_and_bot(d):
    """Utility to print out top and bottom 5 of a dict"""
    l = sorted(d, key=d.get, reverse=True)
    for w in l[:5]:
        print w, d[w]
    print '...'
    for w in l[-5:]:
        print w, d[w]
        
def inrange(spot,fudge=0):
    """Return (# surely in range, # maybe in range) of spot,
    given spot may move by up to fudge in any coordinate"""
    surecount = 0
    maybecount = 0
    for bot in bots:
        d = dist(bot,spot)
        if d <= bot[0]+3*fudge:
            maybecount += 1
        if d <= bot[0]:
            surecount += 1
    return (surecount, maybecount)

# Find range of coordinates
min_coord = [1000000000]*4
max_coord = [0]*4
coords = ['r','x','y','z']

for bot in bots:
    for i in range(4):
        if bot[i] < min_coord[i]:
            min_coord[i] = bot[i]
        if bot[i] > max_coord[i]:
            max_coord[i] = bot[i]

maxrange = 0
for i in range(4):
    print coords[i],':',min_coord[i],'to',max_coord[i]
    maxrange = max(maxrange,max_coord[i]-min_coord[i])

qfactor = 1
while qfactor < maxrange/2:
    qfactor *= 2

qmin = [c/qfactor for c in min_coord]
qmax = [c/qfactor+1 for c in max_coord]

newspots = []
for x in range(qmin[1],qmax[1]+1):
    for y in range(qmin[2],qmax[2]+1):
        for z in range(qmin[3],qmax[3]+1):
            newspots.append((0,x*qfactor,y*qfactor,z*qfactor))

try:
    best_sure = int(sys.argv[2])
except:
    best_sure = 0

TOO_BIG = 400
# DISCARDING ALL POSSIBLE SPOTS THAT ARE NOT IN THE TOP 400
# CLOSEST TO THE ORIGIN. Use second argument to control this value.

round = 0
while qfactor > 0:
    delta = qfactor/2
    spots = []
    for (r,x,y,z) in newspots:
        spots.append((r,x,y,z))
        spots.append((r,x+delta,y,z))
        spots.append((r,x,y+delta,z))
        spots.append((r,x+delta,y+delta,z))
        spots.append((r,x,y,z+delta))
        spots.append((r,x+delta,y,z+delta))
        spots.append((r,x,y+delta,z+delta))
        spots.append((r,x+delta,y+delta,z+delta))

    print '-'*20
    print '%2d' % round,'Considering',len(spots),'spaced by',qfactor
    maybecounts = {}
    for s in spots:
        (sure,maybe) = inrange(s,fudge = qfactor/2)
        best_sure = max(best_sure,sure)
        maybecounts[s] = maybe

    print 'Best sure count:',best_sure

    newspots = []
    potential = []
    for k in maybecounts:
        if maybecounts[k] >= best_sure:
            newspots.append(k)
            potential.append(maybecounts[k])
    newcount = len(newspots)
    print 'Keeping',newcount,'of',len(spots)
    potential.sort()
    print 'Potential counts'
    for i in range(0,len(potential),max(len(potential)/10,1)):
        print potential[i],
    print potential[-1]

    if newcount > TOO_BIG:
        # discard potential answers that are far away from 0
        # so the program might actually finish
        newspots.sort(key=norm)
        newspots = newspots[:TOO_BIG]
        print 'Discarding',newcount - TOO_BIG,'spots.'
    qfactor = qfactor/2
    round += 1

print 'Closest spots:'
for s in newspots:
    print s

bestd = 1000000000000
for s in newspots:
    d = dist((0,0,0,0),s)
    if d < bestd:
        bestd = d
        bestspot = s

print 'Best spot is',bestspot,'at distance',bestd,'in range of',inrange(bestspot)[0]
