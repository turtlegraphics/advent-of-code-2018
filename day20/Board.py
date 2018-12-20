class Cell:
    def __init__(self,loc,val='.'):
        self.val = val
        self.neighbors = [None]*4
        self.loc = loc

    def __str__(self):
        return self.val

class Board:
    def __init__(self):
        self.start = Cell((0,0),'X')
        self.cells = {(0,0):self.start}

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
            for x in range(minx,maxx+1):
                if (x,y) in self.cells:
                    out += str(self.cells[(x,y)])
            out += '\n'
        return out[:-1]

if __name__=='__main__':
    b = Board()
    print b



    
