import sys

filename = 'input.txt'
if len(sys.argv) > 1:
    filename = sys.argv[1]

data = open(filename).readlines()

xclay = []
yclay = []

for line in data:
    fix,move = line.split(',')
    if fix[0] == 'x':
        x = int(fix[2:])
        move = move.strip('\n y=')
        start,ignore,finish = move.split('.')
        for y in range(int(start),int(finish)+1):
            xclay.append(x)
            yclay.append(y)
    else:
        y = int(fix[2:])
        move = move.strip('\n x=')
        start,ignore,finish = move.split('.')
        for x in range(int(start),int(finish)+1):
            xclay.append(x)
            yclay.append(y)

mx = min(xclay)-1
miny = min(yclay)
xclay = [x - mx for x in xclay]
print 'x:',min(xclay),'-',max(xclay)
print 'y:',miny,'-',max(yclay)

xwidth = max(xclay) + 2

ground = []
for row in range(max(yclay)+1):
    ground.append(['.']*xwidth)

for i in range(len(xclay)):
    ground[yclay[i]][xclay[i]] = '#'

def dump(step,flowing):
    out = (step % 200 == 0)
    water = 0
    standing = 0
    for y in range(len(ground)):
        if out:
            print ''.join(ground[y])
        if y >= miny:
            for c in ground[y]:
                if c == '~':
                    water += 1
                    standing += 1
                if c == '|':
                    water += 1
    if out:
        print 'Step:',step,'Flowing:',len(flow),'Total water:',water,'Standing:',standing

# Start the well
ground[0][500-mx] = '|'
flow = [(500-mx,0)] # List of squares where water is flowing

step = 0
while True:
    dump(step,len(flow))
    newflow = []
    for (x,y) in flow:
        if y+1 >= len(ground):
            newflow.append((x,y))
            continue
        if ground[y][x] != '|':
            continue
        if ground[y+1][x] == '|':
            newflow.append((x,y))
        if ground[y+1][x] == '.':
            ground[y+1][x] = '|'
            newflow.append((x,y))
            newflow.append((x,y+1))
        if ground[y+1][x] in ['#','~']:
            leftx = x-1
            while ground[y][leftx] != '#' and ground[y+1][leftx] in ['#','~']:
                leftx -= 1
            rightx = x+1
            while ground[y][rightx] != '#' and ground[y+1][rightx] in ['#','~']:
                rightx += 1

            if ground[y][leftx] == '#' and ground[y][rightx] == '#':
                # stable
                fx = leftx + 1
                while fx < rightx:
                    ground[y][fx] = '~'
                    fx += 1
            else:
                # unstable
                fx = leftx + 1
                while fx < rightx:
                    if ground[y][fx] == '.':
                        ground[y][fx] = '|'
                        newflow.append((fx,y))
                    fx += 1
                if ground[y][leftx] not in ['#','|']:
                    ground[y][leftx] = '|'
                    newflow.append((leftx,y))
                if ground[y][rightx] not in ['#','|']:
                    ground[y][rightx] = '|'
                    newflow.append((rightx,y))

    flow = newflow
    step += 1
