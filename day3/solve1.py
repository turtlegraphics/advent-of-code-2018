import sys
import re

filename = 'input.txt'
if len(sys.argv) > 1:
    filename = sys.argv[1]

data = open(filename).readlines()

claims = []
for line in data:
    claims.append([int(s) for s in filter(None,re.split('#| |,|x|@|:|\n',line))])

maxx = 0
maxy = 0
for claim in claims:
    (id,left,top,width,height) = claim
    maxx = max(maxx,left+width)
    maxy = max(maxy,top+height)
print 'Max:',maxx,maxy

def test(point,claim):
    """Returns True if point is in claim"""
    (id,left,top,width,height) = claim
    (x,y) = point
    return (x >= left) and (x-left < width) and (y >= top) and (y-top < height)

# claim format:  #123 @ 3,2: 5x4
def is_twice(point):
    found = False
    for claim in claims:
        if test(point,claim):
            if found:
                # second time
                return 1
            else:
                found = True
    return 0

count = 0
for x in range(1002):
    for y in range(1002):
        count += is_twice((x,y))
        
print count

