class Recipe:
    def __init__(self,score):
        self.score = score
        self.next = self
        self.prev = self

    def __str__(self):
        return str(self.score)

a1 = Recipe(3)
a2 = Recipe(7)
a1.next = a2
a1.prev = a2
a2.next = a1
a2.prev = a1

board = a1
tail = a2
elf1 = a1
elf2 = a2

def printboard():
    out = ''
    r = board
    while True:
        if r == elf1:
            out += '('
        if r == elf2:
            out += '['
        if r not in [elf1,elf2]:
            out += ' '

        out += str(r)

        if r == elf1:
            out += ')'
        if r == elf2:
            out += ']'
        if r not in [elf1,elf2]:
            out += ' '

        r = r.next
        if r == board:
            break
    print out

def update():
    mix = elf1.score + elf2.score

printboard()
