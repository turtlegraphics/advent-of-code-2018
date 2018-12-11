def power(x,y,serial):
    rack = x + 10
    power = (rack * y + serial)*rack
    hundo = (power/100) % 10
    return hundo - 5


def dump(size,serial):
    for y in range(size):
        out =''
        for x in range(size):
            out += '%3d ' % power(x+1,y+1,serial)
        print out

def tuple(x,y,n,serial):
    tot = 0
    for i in range(n):
        for j in range(n):
           tot += power(x+i,y+j,serial)
    return tot

class Grid:
    def __init__(self,size):
        self.size = size
        self.rack = []
        for y in range(self.size):
            self.rack.append([x + 11 for x in range(self.size)])

    def __str__(self):
        out = ''
        return out

print power(3,5,8)
print power(122,79,57)
print power(217,196,39)
print power(101,153,71)

print tuple(33,45,3,18)
print tuple(21,61,3,42)

omaxv = 0

for n in range(1,15):
    maxv = 0
    for x in range(1,300-(n-2)):
        for y in range(300-(n-2)):
            t = tuple(x,y,n,8772)
            if t > maxv:
                maxv = t
                maxp = (x,y)
    if maxv > omaxv:
        omaxv = maxv
        omaxn = n
        omaxp = maxp
        print '*',
    print n,':',maxv,maxp

print 'Overall'
print omaxp,omaxn,'value',omaxv
