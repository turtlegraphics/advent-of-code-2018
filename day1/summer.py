import sys
data = open('input.txt').readlines()

changes = [int(d) for d in data]

sum = 0
vals = set()
vals.add(0)
loop = 0
while True:
    loop += 1
    print 'Pass: ',loop

    for d in changes:
        sum += d
        if sum in vals:
            print 'found',sum
            sys.exit()
        vals.add(sum)
    print 'total:',sum
