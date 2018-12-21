class Cell:
    def __init__(self,loc):
        self.neighbors = {'N':None,'S':None,'E':None,'W':None}
        self.loc = loc

    def __str__(self):
        return self.val

class Board:
    delta = {'N':(0,-1),'S':(0,1),'E':(1,0),'W':(-1,0)}
    opposite = {'N':'S','S':'N','E':'W','W':'E'}
    def __init__(self):
        self.cells = {(0,0):Cell((0,0))}
        self.position = (0,0)

    def move(self,direction):
        (x,y) = self.position
        (dx,dy) = Board.delta[direction]
        newpos = (x+dx,y+dy)
        if newpos not in self.cells:
            self.cells[newpos] = Cell(newpos)

        self.cells[newpos].neighbors[Board.opposite[direction]] = self.position
        self.cells[self.position].neighbors[direction] = newpos
        
        self.position = newpos

    def __str__(self):
        minx = 0
        maxx = 0
        miny = 0
        maxy = 0
        for (x,y) in self.cells:
            if x < minx:
                minx = x
            if x > maxx:
                maxx = x
            if y < miny:
                miny = y
            if y > maxy:
                maxy = y
        out = ''
        for y in range(miny,maxy+1):
            above = ''
            row = ''
            for x in range(minx,maxx+1):
                above += '#'
                if (x,y) in self.cells:
                    if self.cells[(x,y)].neighbors['W']:
                        row += ' '
                    else:
                        row += '?'

                    if self.cells[(x,y)].neighbors['N']:
                        above += ' '
                    else:
                        above += '?'

                    row += 'X' if self.position == (x,y) else 'o'
                else:
                    above += '?'
                    row += '??'
            above += '#\n'
            row += '?\n'
            out += above + row
        out += '#'+'?#'*(maxx-minx+1)
        return out

if __name__=='__main__':
    b = Board()
    b.move('N')
    b.move('E')
    b.move('S')
    b.move('W')
    b.move('W')
    print b



    
