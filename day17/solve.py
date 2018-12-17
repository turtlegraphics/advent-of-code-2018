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
xclay = [x - mx for x in xclay]
print 'x:',min(xclay),'-',max(xclay)
print 'y:',min(yclay),'-',max(yclay)

xwidth = max(xclay) + 2

ground = []
for row in range(max(yclay)+1):
    ground.append(['.']*xwidth)

for i in range(len(xclay)):
    ground[yclay[i]][xclay[i]] = '#'

ground[0][500-mx] = '+'

for row in ground:
    print ''.join(row)



