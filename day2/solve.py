import sys
from collections import Counter

filename = 'input.txt'
if len(sys.argv) > 1:
    filename = sys.argv[1]

data = open(filename).readlines()

twos = 0
threes = 0
for line in data:
    counts = Counter(list(line.strip()))
    if 2 in counts.values():
        twos += 1
        print 'has 2'
    if 3 in counts.values():
        threes += 1
        print 'has 3'

print twos, threes, twos*threes

for line in data:
    for comp in data:
        count = sum(1 for a, b in zip(line, comp) if a != b)
        if count == 1:
            print line
