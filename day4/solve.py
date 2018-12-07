import sys
import datetime

filename = 'input.txt'
if len(sys.argv) > 1:
    filename = sys.argv[1]

data = open(filename).readlines()

class Guard:
    def __init__(self,id):
        self.id = id
        self.times = [0]*60
        self.status = 'off'

    def begin(self):
        self.status = 'awake'
        self.minute = 0

    def sleep(self,min):
        self.status = 'asleep'
        self.fell = min

    def wake(self,min):
        self.status = 'awake'
        for t in range(self.fell,min):
            self.times[t] += 1

    def __str__(self):
        return 'Guard #'+str(self.id)

    def sleepstr(self):
        ss = ''
        for t in range(60):
            if self.times[t] == 0:
                ss += '.'
            elif self.times[t] < 10:
                ss += str(self.times[t])
            else:
                ss += chr(ord('A') + self.times[t] - 10)
        return ss

    def sleepcount(self):
        count = 0
        for t in range(60):
            count += self.times[t]
        return count

    def maxminute(self):
        maxv = -1
        maxt = -1
        for t in range(60):
            if self.times[t] > maxv:
                maxt = t
                maxv = self.times[t]
        return (maxt,maxv)

notes = []
for line in data:
    stampstr = line[1:17]
    stamp = datetime.datetime.strptime(stampstr,"%Y-%m-%d %H:%M")
    inst = line[19:]
    notes.append((stamp,inst))

guards = {}

notes.sort()
guard = None

for n in notes:
    (stamp, inst) = n
    minute = stamp.minute
    if inst[0] == 'G':
        gid = int(inst[7:11])
        if gid in guards:
            guard = guards[gid]
        else:
            guard = Guard(gid)
            guards[gid] = guard
    elif inst[0] == 'f':
        guard.sleep(minute)
    elif inst[0] == 'w':
        guard.wake(minute)
    else:
        raise('hell')

for gid in guards.keys():
    print "%4d" % (guards[gid].sleepcount()),
    print "%4d" % gid,
    print "%8s" % str(guards[gid].maxminute()),
    print guards[gid].sleepstr()
