import sys

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
        """Return the board at position pos = (x,y)"""
        return self.board[pos[1]][pos[0]]

    def __setitem__(self,pos,val):
        """Set the board at position pos = (x,y) to val"""
        self.board[pos[1]][pos[0]] = val
        
    def __iter__(self):
        for y in range(self.height):
            for x in range(self.width):
                yield( (x,y) )

    def neighbors(self,x,y):
        """Return a list of valid neighbors of (x,y)"""
        n = []
        if x-1 > 0 and self[x-1,y] != '#':
            n.append( (x-1,y) )
        if x+1 < self.width and self[x+1,y] != '#':
            n.append( (x+1,y) )
        if y-1 > 0 and self[x,y-1] != '#':
            n.append( (x,y-1) )
        if y+1 < self.height and self[x,y+1] != '#':
            n.append( (x,y+1) )
        return n

    def __str__(self):
        out = str(self.width) + 'x' + str(self.height)
        for row in self.board:
            out += '\n'
            out += ''.join([str(s) for s in row])
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

    def distances(self,which):
        """mark board with distance from units on the list which"""
        pass

g  = Game(data)
print(g)
print 'elves'
print g.units(['E'])
print 'goblins'
print g.units(['G'])
print 'both'
print g.units(['G','E'])
