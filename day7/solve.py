import sys
import string

filename = 'input.txt'
if len(sys.argv) > 1:
    filename = sys.argv[1]

class JobQ:
    def __init__(self,filename):
        data = open(filename).readlines()
        self.prereq = {}
        for line in data:
            if line[36] in self.prereq:
                self.prereq[line[36]].append(line[5])
            else:
                self.prereq[line[36]] = [line[5]]
            if line[5] not in self.prereq:
                self.prereq[line[5]] = []

    def findsteps(self):
        """Return available jobs or None"""
        todo = []
        for k in self.prereq.keys():
            if self.prereq[k] == []:
                todo.append(k)
        if todo == []:
            return None
        todo.sort()
        return todo
    
    def finished(self,step):
        """Step finished, remove it from prereqs"""
        del self.prereq[step]
        
        for k in self.prereq.keys():
            if step in self.prereq[k]:
                self.prereq[k].remove(step)

work = JobQ(filename)

class Elves:
    def __init__(self,elves):
        self.elves = elves
        self.time = [0]*elves
        self.job = [None]*elves
        self.finished = ''

    def findelf(self):
        """return the number of an idle elf, or None"""
        for e in range(self.elves):
            if self.job[e] == None:
                return e
        return None

    def assign(self,e,job):
        self.time[e] = 60 + ord(job) - 64
        self.job[e] = job
#        print 'assigned',job,'to elf',e

    def inprogress(self):
        """Return list of jobs in progress"""
        ip = []
        for e in range(self.elves):
            if self.job[e] != None:
               ip.append(self.job[e])
        return ip

    def work(self):
        for e in range(self.elves):
            if self.job[e]:
                print self.job[e],self.time[e],'\t',
                self.time[e] -= 1
                if self.time[e] == 0:
                    work.finished(self.job[e])
                    self.finished += self.job[e]
                    self.job[e] = None
            else:
                print '-','-','\t',

    def working(self):
        for e in range(self.elves):
            if self.job[e]:
                return True
        return False

elves = Elves(5)
clock = 0

jobs = work.findsteps()
while jobs:
    # Build list of jobs that need to be assigned
    needed = []
    for j in jobs:
        if j not in elves.inprogress():
            needed.append(j)
    needed.sort()

    # Assign jobs if possible
    while needed and elves.findelf() != None:
        e = elves.findelf()
        elves.assign(e,needed[0])
        needed.remove(needed[0])

    # Do work
    print clock,'\t',
    elves.work()
    clock += 1
    print elves.finished
    jobs = work.findsteps()

print clock





