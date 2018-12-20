import sys

class Node:
    def __init__(self,val = None):
        self.val = val
        self.children = []

    def add_child(self,child):
        self.children.append(child)

class NodeLeaf(Node):
    def __str__(self):
        return self.val

class NodeOr(Node):
    def __str__(self):
        out = '('
        for c in self.children:
            out += str(c) + '|'
        out = out[:-1] + ')'
        return out

class NodeAnd(Node):
    def __str__(self):
        out = ''
        for c in self.children:
            out += str(c)
        return out

class Parser:
    def __init__(self,path):
        self.path = path
        self.current = 1
        self.root = self.parse_and(0)

    def debug_out(self,who,depth):
        print '-'*depth+who,'self.current=',self.current,
        print 'token=',self.path[self.current]

    def parse_leaf(self,depth):
        self.debug_out('leaf',depth)
        val = ''
        while self.path[self.current] in 'NSEW':
            val += self.path[self.current]
            self.current += 1
        return NodeLeaf(val)

    def parse_or(self,depth):
        self.debug_out('or  ',depth)
        assert(self.path[self.current] == '(')
        self.current += 1  # eat (
        me = NodeOr()

        me.add_child(self.parse_and(depth+1))
        while self.path[self.current] == '|':
            self.current += 1  # eat |
            me.add_child(self.parse_and(depth+1))

        self.current += 1 # eat )
        return me

    def parse_and(self,depth):
        self.debug_out('and ',depth)
        me = NodeAnd()
        while self.path[self.current] not in ')|$':
            if self.path[self.current] == '(':
                me.add_child(self.parse_or(depth+1))
            else:
                me.add_child(self.parse_leaf(depth+1))
        return me

# Input goes deep!
sys.setrecursionlimit(3000)

filename = sys.argv[1]
data = open(filename).readlines()
input = ''.join([line.strip() for line in data])
print input
check = '^' + str(Parser(input).root) + '$'
if check == input:
    print 'Got it!'

