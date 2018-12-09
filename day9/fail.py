import sys

if len(sys.argv) != 3:
    print 'solve players marbles'
    sys.exit()

players = int(sys.argv[1])
marbles = int(sys.argv[2])    

print players,'players',marbles,'marbles'

class Circle:
    def __init__(self):
        self.current = 0
        self.circle = []

    def __str__(self):
        out = ''
        for i in range(len(self.circle)):
            if i == self.current:
                out += '('+str(self.circle[i])+')'
            else:
                out += ' '+str(self.circle[i])+' '
        return out

    def add(self,val):
        if self.circle == []:
            self.circle = [val]
            return
        spot = self.current + 1
        if spot > len(self.circle):
            spot = spot % len(self.circle)
        front = list(self.circle[:spot+1])
        back = list(self.circle[spot+1:])
        self.circle = front + [val] + back
        self.current = len(front)

game = Circle()
for m in range(marbles):
    game.add(m)
    print game
