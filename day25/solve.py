import sys

if len(sys.argv) > 1:
    filename = sys.argv[1]
data = open(filename).readlines()
points = [tuple([int(x) for x in l.strip().split(',')]) for l in data]

components = []

def dist(p1,p2):
    (x1,y1,z1,w1) = p1
    (x2,y2,z2,w2) = p2
    return abs(x1-x2) + abs(y1-y2) + abs(z1-z2) + abs(w1-w2)

def inconst(p,c):
    """Check if point p in constellation c"""
    for q in c:
        if dist(p,q) <= 3:
            return True
    return False

constellations = []
for p in points:
    belongs = []
    for c in constellations:
        if inconst(p,c):
            belongs.append(c)
    if len(belongs) == 0:
        constellations.append([p])
    elif len(belongs) == 1:
        belongs[0].append(p)
    else:
        # belongs to more than one
        for b in belongs[1:]:
            belongs[0].extend(b)
            constellations.remove(b)
        belongs[0].append(p)

print len(constellations)
