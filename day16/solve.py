import sys

samplefile = sys.argv[1]
data = open(samplefile).readlines()
codefile = sys.argv[2]
code = open(codefile).readlines()

class Machine:
    def __init__(self):
        self.regs = [0,0,0,0]

        self.ops = [self.addr, self.addi, self.mulr, self.muli,
                    self.banr, self.bani, self.borr, self.bori,
                    self.setr, self.seti,
                    self.gtir, self.gtri, self.gtrr,
                    self.eqir, self.eqri, self.eqrr]

    def __str__(self):
        return str(self.regs)

    def load(self,regs):
        for i in range(4):
            self.regs[i] = regs[i]

    def test(self,regs):
        """Check current state against passed values"""
        for i in range(4):
            if self.regs[i] != regs[i]:
                return False
        return True

    def addr(self,a,b,c):
        self.regs[c] = self.regs[a] + self.regs[b]
    def addi(self,a,b,c):
        self.regs[c] = self.regs[a] + b

    def mulr(self,a,b,c):
        self.regs[c] = self.regs[a] * self.regs[b]
    def muli(self,a,b,c):
        self.regs[c] = self.regs[a] * b

    def banr(self,a,b,c):
        self.regs[c] = self.regs[a] & self.regs[b]
    def bani(self,a,b,c):
        self.regs[c] = self.regs[a] & b

    def borr(self,a,b,c):
        self.regs[c] = self.regs[a] | self.regs[b]
    def bori(self,a,b,c):
        self.regs[c] = self.regs[a] | b

    def setr(self,a,b,c):
        self.regs[c] = self.regs[a]
    def seti(self,a,b,c):
        self.regs[c] = a

    def gtir(self,a,b,c):
        self.regs[c] = 1 if a > self.regs[b] else 0
    def gtri(self,a,b,c):
        self.regs[c] = 1 if self.regs[a] > b else 0
    def gtrr(self,a,b,c):
        self.regs[c] = 1 if self.regs[a] > self.regs[b] else 0

    def eqir(self,a,b,c):
        self.regs[c] = 1 if a == self.regs[b] else 0
    def eqri(self,a,b,c):
        self.regs[c] = 1 if self.regs[a] == b else 0
    def eqrr(self,a,b,c):
        self.regs[c] = 1 if self.regs[a] == self.regs[b] else 0

m = Machine()

icount = 0

possible = {}
for op in m.ops:
    possible[op] = range(16)

for record in range(0,len(data),3):
    before = eval(data[record][8:])
    inst = [int(x) for x in data[record+1].split()]
    after = eval(data[record+2][8:])

    opcount = 0
    for op in m.ops:
        m.load(before)
        op(inst[1],inst[2],inst[3])
        if m.test(after):
            # could be this op
            opcount += 1
            # print 'B:',before,'I:',inst,'A:'
        else:
            # cannot be this op
            try:
                possible[op].remove(inst[0])
            except ValueError:
                pass

    if opcount >= 3:
        icount += 1

print 'Operations with > 3 interpretations:',icount

truth = {}

while len(truth) < 16:
    for op in possible:
        if len(possible[op]) == 1:
            # sure about this one
            truth[op] = possible[op][0]

    for op in truth:
        try:
            del possible[op]
            for k in possible:
                try:
                    possible[k].remove(truth[op])
                except:
                    pass
        except:
            pass

opcode = {}
for op in truth:
    opcode[truth[op]] = op

print
print 'Opcodes:'
for c in opcode:
    print c,str(opcode[c]).split('.')[1][:4]

m.load([0,0,0,0])
for line in code:
    o,a,b,c = [int(x) for x in line.split()]
    opcode[o](a,b,c)

print m
