import sys
P = 15466939
Q = 65899

target = 1

def clamp(x):
    return x & 0xFFFFFF

r4 = 0
r5 = 0

halting = set()
last = None

while True:
    r4 = 0x10000 | r5
    r5 = P
    while True:
        r3 = r4 % 256
#        print '%9d %9d %9d' % (r3,r4,r5)
        r5 = r5 + r3
        r5 = clamp(Q*clamp(r5))
        if r4 < 256:
            # r5 is now a winning number, that will halt
            if not last:
                print 'First input that halts (part 1 solution):',r5
            if r5 in halting:
                print 'seen',r5,'before.'
                print 'Last before the repeat (part 2 solution):',last
                sys.exit()
            halting.add(r5)
            last = r5
            if len(halting) % 1000 == 0:
                print 'Found',len(halting),'halting inputs.'
            break
        r4 = r4 / 256



