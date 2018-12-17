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

ground[0][500-mx] = '|'

def dump(forceout, step,flowing):
    out = (step % 200 == 0) | forceout
    water = 0
    for y in range(len(ground)):
        if out:
            print ''.join(ground[y])
        if y >= miny:
            for c in ground[y]:
                if c in ['|','~']:
                    water += 1
    if out:
        print 'Step:',step,'Flowing:',len(flow),'Total water:',water
    return water

# List of squares where water is flowing
flow = [(500-mx,0)]

step = 0
oldwater = -1
water = 0
oldflow = 0
flowcount = len(flow)
#while (water != oldwater) | (flowcount != oldflow):
while True:
    oldwater = water
    oldflow = len(flow)
    water = dump(False,step,oldflow)
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

dump(True,step,len(flow))
