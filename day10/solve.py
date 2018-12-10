import sys

filename = 'input.txt'
if len(sys.argv) > 1:
    filename = sys.argv[1]

data = open(filename).readlines()

x = []
y = []
dx = []
dy = []

for line in data:
    val = line.split()
    x.append( (int(val[0]) ) )
    y.append( (int(val[1]) ) )
    dx.append( (int(val[2]) ) )
    dy.append( (int(val[3]) ) )

points = len(x)


def display():
    nx = [v - min(x) for v in x]
    ny = [v - min(y) for v in y]
    for l in range(max(ny)+1):
        row = [' ']*(max(nx)+1)
        for i in range(points):
            if ny[i] == l:
                row[nx[i]] = '#'
        print ''.join(row)

step = 0
while step < 11000:
    xrange = max(x) - min(x)
    yrange = max(y) - min(y)
    
    if step == 10515:
        print step, 'X:',xrange,'Y:',yrange
        print min(x),max(x)
        print min(y),max(y)
        display()
        break

    for i in range(points):
        x[i] += dx[i]
        y[i] += dy[i]

    step += 1

