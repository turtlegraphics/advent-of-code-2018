board = [3,7]
elf1 = 0
elf2 = 1

def printboard():
    out = ''
    for r in range(len(board)):
        if r == elf1:
            out += '('
        if r == elf2:
            out += '['
        if r not in [elf1,elf2]:
            out += ' '

        out +=  str(board[r])

        if r == elf1:
            out += ')'
        if r == elf2:
            out += ']'
        if r not in [elf1,elf2]:
            out += ' '

    print out

def update():
    mix = [int(x) for x in str(board[elf1] + board[elf2])]
    board.extend(mix)

def move(elf):
    return (elf + 1 + board[elf]) % len(board)

printboard()

goal = '681901'
chunk = 10000
while True:
    update()
    elf1 = move(elf1)
    elf2 = move(elf2)
    if len(board) % chunk == 0:
        print len(board)
        tail = ''.join(str(x) for x in board[-chunk-11:])
        found = tail.find(goal)
        if found >= 0:
            print 'Found',found+len(board)-chunk-11
            break

#    printboard()


#print ''.join([str(x) for x in board[goal:goal+10]])
