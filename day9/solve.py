import sys

if len(sys.argv) != 3:
    print 'solve players marbles'
    sys.exit()

players = int(sys.argv[1])
marbles = int(sys.argv[2])    

print players,'players',marbles,'marbles'

class Marble:
    def __init__(self,val):
        self.val = val
        self.next = None

    def __str__(self):
        return str(self.val)

class Circle:
    def __init__(self):
        self.first = None
        self.current = None

    def __str__(self):
        if self.first == None:
            return '--empty--'

        out = ''
        cur = self.first

        if cur == self.current:
            out += '('+str(cur)+')'
        else:
            out += ' '+str(cur)+' '
        cur = cur.next

        while cur != self.first:
            if cur == self.current:
                out += '('+str(cur)+')'
            else:
                out += ' '+str(cur)+' '
            cur = cur.next

        return out

    def add(self,marble):
        if self.current == None:
            self.first = marble
            self.current = marble
            marble.next = marble
            return

        spot = self.current.next
        marble.next = spot.next
        spot.next = marble
        self.current = marble

game = Circle()
for m in range(marbles):
    game.add(Marble(m))
    print game
