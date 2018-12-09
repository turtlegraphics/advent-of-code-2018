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
        self.next = self
        self.prev = self

    def __str__(self):
        return str(self.val)

    def is_special(self):
        return self.val % 23 == 0

class Circle:
    def __init__(self):
        self.first = Marble(0)
        self.current = self.first

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
        if marble.is_special():
            score = marble.val
            take = self.current.prev.prev.prev.prev.prev.prev.prev
            score += take.val
            self.current = take.next
            take.prev.next = take.next
            take.next.prev = take.prev
            return score

        # not special :-(
        spot = self.current.next
        spot.next.prev = marble
        marble.next = spot.next
        marble.prev = spot
        spot.next = marble
        self.current = marble

        return 0 # no score

game = Circle()
player = 0
scores = [0]*players

for m in range(marbles+1)[1:]:
   scores[player] += game.add(Marble(m))
   player = (player + 1) % players

print scores
print max(scores)
