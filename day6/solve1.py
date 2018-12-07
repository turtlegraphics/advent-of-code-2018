import sys

filename = 'input.txt'
if len(sys.argv) > 1:
    filename = sys.argv[1]

data = open(filename).readlines()

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def dist(self,p):
        return abs(self.x - p.x) + abs(self.y - p.y)

points = []
for line in data:
    cstr = line.split(', ')
    (x,y) = int(cstr[0]),int(cstr[1])
    points.append(Point(x,y))

print min([p.x for p in points])
print max([p.x for p in points])
print min([p.y for p in points])
print max([p.y for p in points])

class Grid:
    def __init__(self,size):
        self.grid = []
        for i in range(size):
            row = [-1]*size
            self.grid.append(row)
    
    def __str__(self):
        s = ''
        for r in self.grid:
            for v in r:
                if v < 0:
                    s += '.'
                else:
                    s += str(v)
            s+='\n'
        return s

    def is_infinite(self,v):
        if v in self.grid[0] or v in self.grid[size-1]:
            return True
        for r in self.grid:
            if v == r[0] or v == r[size-1]:
                return True
        return False

size = 400
grid = Grid(size)

for x in range(size):
    for y in range(size):
        bestd = 3*size
        bestp = -1
        for p in range(len(points)):
            d = points[p].dist(Point(x,y))
            if d == bestd:
                bestp = -1
            elif d < bestd:
                bestd = d
                bestp = p
        grid.grid[y][x] = bestp

counts = {}
for p in range(len(points)):
    counts[p] = 0
counts[-1] = 0

for x in range(size):
    for y in range(size):
        counts[grid.grid[y][x]] += 1
    
finite = []
for p in range(len(points)):
    if not grid.is_infinite(p):
        finite.append((counts[p],p))
finite.sort()
print finite

