import sys
from collections import deque
from box import *

class Game:
    def __init__(self,lines,elfpower):
        self.board = []
        self.combatants = {Elf:0, Gnome:0}
        for line in lines:
            row = []
            for c in line.strip():
                if c == '#':
                    row.append(Wall())
                elif c == '.':
                    row.append(Empty())
                elif c == 'E':
                    row.append(Elf(elfpower))
                    self.combatants[Elf] += 1
                elif c == 'G':
                    row.append(Gnome())
                    self.combatants[Gnome] += 1

            self.board.append(row)
        self.width = len(self.board[0])
        self.height = len(lines)

    def __getitem__(self, pos):
        """Return the board at position pos = (y,x)"""
        return self.board[pos[0]][pos[1]]

    def __setitem__(self,pos,val):
        """Set the board at position pos = (y,x) to val"""
        self.board[pos[0]][pos[1]] = val
        
    def __iter__(self):
        for y in range(self.height):
            for x in range(self.width):
                yield( (y,x) )

    def units(self,race):
        """Iterate over units of a given race: Elf, Gnome, or Unit = both."""
        for pos in self:
            if isinstance(self[pos],race):
                yield(pos)

    def neighbors(self,pos):
        """Return a list of valid neighbors of pos"""
        (y,x) = pos
        n = []
        if y-1 > 0 and not isinstance(self[y-1,x],Wall):
            n.append( (y-1,x) )
        if x-1 > 0 and not isinstance(self[y,x-1],Wall):
            n.append( (y,x-1) )
        if x+1 < self.width and not isinstance(self[y,x+1],Wall):
            n.append( (y,x+1) )
        if y+1 < self.height and not isinstance(self[y+1,x],Wall):
            n.append( (y+1,x) )
        return n

    def __str__(self):
        out = 'Elves: '+str(self.combatants[Elf])
        out += '\tGnomes: '+str(self.combatants[Gnome])
        for y in range(self.height):
            out += '\n'
            for x in range(self.width):
                v = self[y,x]
                if isinstance(v,int) and v >= 10:
                    c = 'X'
                else:
                    c = str(v)
                out += c
        return out

    def inrange(self,race):
        """Mark board with squares one away from all units of type race"""
        for u in self.units(race):
            for n in self.neighbors(u):
                if isinstance(self[n],Empty):
                    self[n] = '?'

    def clean(self):
        """Clean up a messy board."""
        for pos in self:
            if not isinstance(self[pos],Box):
                self[pos] = Empty()

    def distances(self,startpos):
        """mark board with distances from startpos.  returns a list
        of any ? squares found in the form (dist,pos)"""
        self[startpos] = 0
        visit = deque()
        visit.append(startpos)
        targets = [] # list of possible neartest targets
        while visit:
            pos = visit.popleft()
            val = self[pos]
            for n in self.neighbors(pos):
                vn = self[n]
                if isinstance(vn,Empty):
                    self[n] = val+1
                    visit.append(n)
                elif isinstance(vn,int):
                    if vn > val+1:
                        self[n] = val+1
                        visit.append(n)
                elif vn == '?':
                    targets.append((val+1,n))
        return targets

    def choose(self,startpos):
        """Returns the location to move toward, or None"""
        me = self[startpos]
        targets = self.distances(startpos)
        self.clean()
        self[startpos] = me
        try:
            (dist,loc) = min(targets)
        except ValueError:
            return None   # no place to go
        return loc

    def move(self,startpos):
        """Return a move for the unit at startpos, or None."""
        # where do I want to be
        me = self[startpos]
        self.inrange(me.enemy())  # mark board with ?'s for in range squares
        chosen = self.choose(startpos)
        if chosen == None:
            return None

        # find best move
        self.distances(chosen) # mark board with distances to chosen enemy
        moves = []
        for n in self.neighbors(startpos):
            if isinstance(self[n],int):
                moves.append( (self[n], n) )
        (dist,pos) = min(moves)
        self.clean()

        # make the move
        assert(isinstance(self[pos],Empty))
        self[startpos] = Empty()
        self[pos] = me
        me.moved = True

        # try to attack
        self.attack(pos)

    def attack(self,startpos):
        """Make an attack if possible. Return True if attack happened."""
        me = self[startpos]
        bestn = None
        besthp = 300
        for n in self.neighbors(startpos):
            if isinstance(self[n],me.enemy()):
                if self[n].hp < besthp:
                    besthp = self[n].hp
                    bestn = n

        if bestn == None:
            return False

#       print me,'at',startpos,'attacked',self[n],'at',n
        killed = self[bestn].hurt(me.power)
        if killed:
#           print me,'killed',self[n],'!!!!'
            if me.enemy() == Elf:
                deadelf()

            self.combatants[me.enemy()] -= 1
            self[bestn] = Empty()

        return True

    def victor(self):
        if self.combatants[Elf] == 0:
            return Gnome
        elif self.combatants[Gnome] == 0:
            return Elf
        return None

def fight(g):
    round = 0

    while not g.victor():
        print 'round',round
        print(g)
        for u in g.units(Unit):
            if g.victor():
                return round
            if not g[u].moved:
                if not g.attack(u):
                    g.move(u)
        round += 1
        for u in g.units(Unit):
            g[u].moved = False

    return round


allow_dead_elves = True
def deadelf():
    """Report a dead elf."""
    if allow_dead_elves:
        return
    sys.stderr.write('AN ELF HAS DIED!!!!\n')
    sys.exit(1)

usage = """
usage:
   solve.py filename [elfpower]
"""

elfpower = 3

try:
    filename = sys.argv[1]
    if len(sys.argv) > 2:
        elfpower = int(sys.argv[2])
        allow_dead_elves = False
except:
    sys.stderr.write(usage)
    sys.exit()

data = open(filename).readlines()
g  = Game(data,elfpower)

rounds = fight(g)

print '='*30
print 'Elves win!' if g.victor() == Elf else 'Gnomes win!'
print(g)

totalhp = 0
for u in g.units(g.victor()):
    totalhp += g[u].hp
print 'Outcome:',rounds,'*',totalhp,'=',rounds*totalhp
