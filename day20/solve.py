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

check = '^' + str(Parser.Parser(input).root) + '$'
if check == input:
    print 'Got it!'

