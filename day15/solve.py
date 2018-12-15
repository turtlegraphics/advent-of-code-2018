import sys
from collections import deque

filename = 'input.txt'
if len(sys.argv) > 1:
    filename = sys.argv[1]

data = open(filename).readlines()

INF = 32768  # "infinity" - bigger than the board

class Game:
    def __init__(self,lines):
        self.board = []
        for line in lines:
            line = line.strip()
            self.board.append(list(line))
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

    def neighbors(self,pos):
        """Return a list of valid neighbors of pos"""
        (y,x) = pos
        n = []
        if y-1 > 0 and self[y-1,x] != '#':
            n.append( (y-1,x) )
        if x-1 > 0 and self[y,x-1] != '#':
            n.append( (y,x-1) )
        if x+1 < self.width and self[y,x+1] != '#':
            n.append( (y,x+1) )
        if y+1 < self.height and self[y+1,x] != '#':
            n.append( (y+1,x) )
        return n

    def __str__(self):
        out = str(self.width) + 'x' + str(self.height)
        for row in self.board:
            out += '\n'
            for v in row:
                if isinstance(v,int):
                    if v >= 10:
                        c = 'X'
                    else:
                        c = str(v)
                else:
                    c = v
                out += c
        return out

    def empty(self,pos):
        return self[pos] == '.'

    def units(self,which):
        """return a list of units, which is a list of types to find"""
        found = []
        for pos in self:
            if self[pos] in which:
                found.append(pos)
        return found

    def inrange(self,which):
        for u in self.units(which):
            for n in self.neighbors(u):
                if self.empty(n):
                    self[n] = '?'

    def clean(self):
        """Clean up a messy board."""
        for pos in self:
            if self[pos] not in ['#','E','G']:
                self[pos] = '.'

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
                if vn == '.':
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
        enemy = 'G' if me == 'E' else 'E'
        self.inrange(enemy)  # mark board with ?'s for in range squares
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
        assert(self[pos] == '.')
        self[startpos] = '.'
        self[pos] = me
        # try to attack
        self.attack(pos)

    def attack(self,startpos):
        """Make an attack if possible. Return True if attack happened."""
        me = self[startpos]
        enemy = 'G' if me == 'E' else 'E'
        for n in self.neighbors(startpos):
            if self[n] == enemy:
                print me,'at',startpos,'attacked',enemy,'at',n
                return True
        return False

g  = Game(data)
while True:
    print(g)
    raw_input()
    for u in g.units(['E','G']):
        if not g.attack(u):
            g.move(u)
            
