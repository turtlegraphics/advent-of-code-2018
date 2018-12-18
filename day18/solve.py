import sys

filename = 'input.txt'
if len(sys.argv) > 1:
    filename = sys.argv[1]

data = open(filename).readlines()

board = []
board.append(['@']*(len(data[0].strip())+2))
for line in data:
    board.append(['@'] + list(line.strip()) + ['@'])
board.append(['@']*(len(data[0].strip())+2))

def dump(state):
    for row in state:
        print ''.join(row)


neighbors = [(-1,-1),(0,-1),(1,-1),
             (-1, 0),       (1, 0),
             (-1, 1),(0, 1),(1, 1)]

def evolve(state):
    newstate = []
    for row in state:
        newstate.append(['?']*len(row))

    for y in range(len(state)):
        for x in range(len(state[y])):
            counts = {'.':0,'|':0,'#':0,'@':0}
            for dx,dy in neighbors:
                try:
                    counts[state[y+dy][x+dx]] += 1
                except:
                    pass
            newstate[y][x] = state[y][x]
            if state[y][x] == '.' and counts['|'] >= 3:
                newstate[y][x] = '|'
            if state[y][x] == '|' and counts['#'] >= 3:
                newstate[y][x] = '#'
            if state[y][x] == '#' and (counts['#'] == 0 or counts['|'] == 0):
                newstate[y][x] = '.'

    return newstate

def value(state):
    counts = {'.':0,'|':0,'#':0,'@':0}
    for y in range(len(state)):
        for x in range(len(state[y])):
            counts[state[y][x]] += 1
    return counts['|']*counts['#']

time = 0
print 'Initial state:'
dump(board)

while time < 2100:
    if time == 10:
        dump(board)
        print 'Time:',time,'Value:',value(board)
    board = evolve(board)
    time += 1
    if time > 2000:
        print 'Time:',time,'Value:',value(board)

dump(board)

