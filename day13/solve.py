import sys
import string
import re

filename = 'input.txt'
if len(sys.argv) > 1:
    filename = sys.argv[1]

data = open(filename).readlines()
track = []
for line in data:
    track.append(list(line.strip('\n')))


def print_track():
    for row in track:
        print ''.join(row)

carts = []

cartheadings = {
    '<':(-1,0),
    '>':(1,0),
    '^':(0,-1),
    'v':(0,1)
    }

cartturns = {
    # Given heading and underneath, which way to go?
    '^/':'>',
    '^\\':'<',
    'v/':'<',
    'v\\':'>',
    '>/':'^',
    '>\\':'v',
    '</':'v',
    '<\\':'^'
}

turnoptions = [
    { # left
        '^':'<',
        '<':'v',
        'v':'>',
        '>':'^'
        },
    { # straight
        '^':'^',
        '<':'<',
        'v':'v',
        '>':'>'
        },
    { # right
        '^':'>',
        '>':'v',
        'v':'<',
        '<':'^'
        }
]
        
class Cart:
    id_counter = 0
    def __init__(self,x,y,heading):
        self.id = Cart.id_counter
        Cart.id_counter += 1
        self.x = x
        self.y = y
        self.heading = heading
        self.underneath = '|'
        if heading in ['<','>']:
            self.underneath = '-'
        self.intersection_count = 0
        self.dead = False

    def move(self):
        """Returns location of crash, if there was one"""
        assert(not self.dead)

        if self.underneath in ['/','\\']:
            self.heading = cartturns[self.heading+self.underneath]

        if self.underneath == '+':
            self.heading = turnoptions[self.intersection_count % 3][self.heading]
            self.intersection_count += 1

        (dx,dy) = cartheadings[self.heading]
        (nx,ny) = (self.x+dx,self.y+dy)
        track[self.y][self.x] = self.underneath
        self.underneath = track[ny][nx]
        if self.underneath in cartheadings:
            print 'Crash! at',(nx,ny)
            self.dead = True
            return (nx,ny)

        track[ny][nx] = self.heading
        self.x = nx
        self.y = ny

    def kill(self):
        """That's about how I feel rn"""
        self.dead = True
        track[self.y][self.x] = self.underneath

    def __str__(self):
        out = 'Cart ' + str(self.id) + ':'
        out += str((self.x,self.y)) + self.heading
        return out

for y in range(len(track)):
    row = track[y]
    for x in range(len(row)):
        if row[x] in cartheadings:
            carts.append(Cart(x,y,row[x]))

t = 0
newcarts = [(c.y,c.x,c) for c in carts]
while True:
    print t
#    print_track()
#    raw_input()
    # sort the goddamn carts
    newcarts.sort()
    carts = [c for (y,x,c) in newcarts]
    newcarts = []
    for c in carts:
        if not c.dead:
            crashed = c.move()
            if crashed:
                cx,cy = crashed
                # find the other cart and kill it
                for d in carts:
                    if d.x == cx and d.y == cy:
                        d.kill()
            else:
                newcarts.append((c.y,c.x,c))

    if len(newcarts) == 1:
        y,x,c = newcarts[0]
        print 'last cart:',y,x,c
        break
    t += 1
    
