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

def overlap(claim1,claim2):
    """Returns True if claims overlap"""
    (id1,left1,top1,width1,height1) = claim1
    (id2,left2,top2,width2,height2) = claim2
    return not (left1+width1 < left2 or left1 > left2+width2 or top1 > top2+height2 or top1+height1 < top2)

def clear(claim):
    """Test if a claim is clear of all others"""
    for c in claims:
        if (c[0]!=claim[0]):
            if overlap(claim,c):
                return False
    return True

for claim in claims:
    if clear(claim):
        print claim

