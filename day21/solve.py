import sys

class Machine:
    def __init__(self,regcount,ipreg,code,debug_level = 0):
        self.regcount = regcount
        self.regs = [0]*self.regcount
        self.ops = [self.addr, self.addi, self.mulr, self.muli,
                    self.banr, self.bani, self.borr, self.bori,
                    self.setr, self.seti,
                    self.gtir, self.gtri, self.gtrr,
                    self.eqir, self.eqri, self.eqrr]
        self.steps = 0
        self.ipreg = ipreg
        self.debug_level = debug_level
        self.code = code
        self.ip = 0

    def __str__(self):
        out = '['
        for r in self.regs:
            out += '%9d' % r + ','
        out = out[:-1] + ']'
        return out

    def reset(self):
        for i in range(self.regcount):
            self.regs[i] = 0

    def load(self,regs):
        for i in range(len(regs)):
            self.regs[i] = regs[i]

    def test(self,regs):
        """Check current state against passed values"""
        for i in range(len(regs)):
            if self.regs[i] != regs[i]:
                return False
        return True

    def setregister(self,reg,value):
        """Called externally to set a single register to a value."""
        self.regs[reg] = value

    def getregister(self,reg):
        """Called externally to read a single register."""
        return self.regs[reg]

    def execute(self,instruction):
        """Execute instruction of form
        oper a b c
        """
        (oper,a,b,c) = instruction.split()
        getattr(self,oper)(int(a),int(b),int(c))

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


    def debug(self):
        """Produce debug output or possibly allow for user intervention"""
        if self.debug_level > 0:
            print self.steps,'ip=',self.ip,self,self.code[self.ip]
        if self.debug_level > 1:
            user = raw_input()
            if user:
                r,v = user.split()
                self.setregister(int(r),int(v))

    def step(self):
        """Execute one step of code"""
        if self.ip >= len(self.code):
            return False
        self.debug()
        self.setregister(self.ipreg,self.ip)
        self.execute(self.code[self.ip])
        self.ip = self.getregister(self.ipreg)
        self.ip += 1
        self.steps += 1
        return True

    def run(self):
        """Set machine to running."""
        while self.step():
            pass

if __name__=='__main__':
    data = [x.strip() for x in open(sys.argv[1]).readlines()]
    code = data[1:]
    ipset,ipval = data[0].split()
    assert(ipset == '#ip')
    ipreg = int(ipval)

    init = int(sys.argv[2])
    print 'Using initial value',init

    m= Machine(regcount=6,ipreg=ipreg,code=code,debug_level=0)
    m.setregister(0,init)

    # view some key steps of the machine
    while m.step():
        if m.ip in [9,10,11,12,13,28]:
            print ('%8d:%2d ' % (m.steps,m.ip)),m

    sys.exit()

    # failed effort to brute force it
    init = 0
    machines = []
    while True:
        # add a new machine with a new init value
        newmachine = Machine(regcount=6,ipreg=ipreg,code=code,debug_level=0)
        newmachine.setregister(0,init)
        machines.append(newmachine)
        init += 1
        for i in range(len(machines)):
            for s in range(1000):
                if not machines[i].step():
                    # it halted!
                    print 'machine',i,'halted after',machines[i].steps,'steps.'
                    sys.exit()
        if init % 10 == 0:
            print init+1,'machines'
