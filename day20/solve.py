import sys
import Node
import Parser

filename = sys.argv[1]
data = open(filename).readlines()
input = ''.join([line.strip() for line in data])
if len(input) > 1000:
    # Input goes deep!
    sys.setrecursionlimit(3000)
else:
    print input

reg = Parser.Parser(input)
check = '^' + str(reg.root) + '$'
if check == input:
    print 'Got it!'

count = 0
for v in reg.root:
#    print v
    count += 1
    if count % 1000 == 0:
        print count

print 'paths:',count


