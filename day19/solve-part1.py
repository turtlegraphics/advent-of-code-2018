import sys

class Machine:
    def __init__(self,regcount,ip = None):
        self.regcount = regcount
        self.regs = [0]*self.regcount
        self.ops = [self.addr, self.addi, self.mulr, self.muli,
                    self.banr, self.bani, self.borr, self.bori,
                    self.setr, self.seti,
                    self.gtir, self.gtri, self.gtrr,
                    self.eqir, self.eqri, self.eqrr]

    def __str__(self):
        return str(self.regs)

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



if __name__=='__main__':
    m = Machine(6)

    #ip 3 was the first line, now its gone
    code = [x.strip() for x in open(sys.argv[1]).readlines()]

    ipreg = 3
    ip = 0
    step = 0

    while ip < len(code):
        print step,'ip=',ip,m,code[ip]
        m.setregister(ipreg,ip)
        m.execute(code[ip])
        ip = m.getregister(ipreg)
        ip += 1
        step += 1

    print 'Final state:'
    print step,'ip=',ip,m
    
