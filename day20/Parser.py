import Node

class Parser:
    def __init__(self,path,debug=False):
        self.debug = debug
        self.path = path
        self.current = 1
        self.root = self.parse_and(0)

    def debug_out(self,who,depth):
        if self.debug:
            print '-'*depth+who,'self.current=',self.current,
            print 'token=',self.path[self.current]

    def parse_leaf(self,depth):
        self.debug_out('leaf',depth)
        val = ''
        while self.path[self.current] in 'NSEW':
            val += self.path[self.current]
            self.current += 1
        return Node.NodeLeaf(val)

    def parse_or(self,depth):
        self.debug_out('or  ',depth)
        assert(self.path[self.current] == '(')
        self.current += 1  # eat (
        me = Node.NodeOr()

        me.add_child(self.parse_and(depth+1))
        while self.path[self.current] == '|':
            self.current += 1  # eat |
            me.add_child(self.parse_and(depth+1))

        self.current += 1 # eat )
        return me

    def parse_and(self,depth):
        self.debug_out('and ',depth)
        me = Node.NodeAnd()
        while self.path[self.current] not in ')|$':
            if self.path[self.current] == '(':
                me.add_child(self.parse_or(depth+1))
            else:
                me.add_child(self.parse_leaf(depth+1))
        return me

if __name__ == '__main__':
    input = '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$'
    print input
    check = '^' + str(Parser(input,debug=True).root) + '$'
    if check == input:
        print 'Got it!'
    else:
        print 'Did not reproduce input.'

