class Node:
    def __init__(self,val = None):
        self.val = val
        self.children = []

    def add_child(self,child):
        self.children.append(child)

class NodeLeaf(Node):
    def __str__(self):
        return self.val

    def __iter__(self):
        yield self.val

    def legal(self,path):
        """Return return a list of remaining suffixes after matching
        (or empty set for no match)."""
        if len(path) >= len(self.val):
            if path[:len(self.val)] == self.val:
                return set([path[len(self.val):]])
            else:
                return set()
        if self.val[:len(path)] == path:
            return set([''])
        return set()

class NodeOr(Node):
    def __str__(self):
        out = '('
        for c in self.children:
            out += str(c) + '|'
        out = out[:-1] + ')'
        return out

    def __iter__(self):
        for c in self.children:
            for s in c:
                yield s

    def legal(self,path):
        """Return return a list of remaining suffixes after matching
        (or empty set for no match)."""
        suffixes = set()
        for c in self.children:
            suffixes |= c.legal(path)
        return suffixes

class NodeAnd(Node):
    def __str__(self):
        out = ''
        for c in self.children:
            out += str(c)
        return out

    def _r_iter(self,kids):
        if len(kids) == 0:
            yield ''
            return
        rest = kids[1:]
        for front in kids[0]:
            for back in self._r_iter(rest):
                yield front + back

    def __iter__(self):
        for v in self._r_iter(self.children):
            yield v

    def legal(self,path):
        """Return return a list of remaining suffixes after matching
        (or empty set for no match)."""
        suffixes = set([path])
        for c in self.children:
            newsuf = set()
            for s in suffixes:
                newsuf |= c.legal(s)
            suffixes = newsuf
        return suffixes

if __name__=='__main__':
    loop = NodeLeaf('NSEW')
    print "testing NodeLeaf:",loop
    for test in ['NSEW','NSE','NW','','NSEWNNNNN']:
        print "'"+test+"'",':',loop.legal(test)

    shimmy = NodeLeaf('NSNS')
    step = NodeOr()
    step.add_child(loop)
    step.add_child(shimmy)
    print "testing NodeOr:",step
    for test in ['NSEW','NSNS','NS','XX','NSXX','NSEWXXX','NSNSXXX']:
        print "'"+test+"'",':',step.legal(test)
        
    null = NodeLeaf('')
    maybe = NodeOr()
    maybe.add_child(shimmy)
    maybe.add_child(null)
    print "testing NodeOr:",maybe
    for test in ['NSEW','NSNS','NS','XX','NSXX','NSEWXXX','NSNSXXX']:
        print "'"+test+"'",':',maybe.legal(test)

    south = NodeLeaf('S')
    north = NodeLeaf('N')
    dance = NodeAnd()
    dance.add_child(south)
    dance.add_child(maybe)
    dance.add_child(step)
    dance.add_child(north)
    print "testing NodeAnd:",dance
    for test in ['X','SN','SNSEWN','SNSNSN','SNS','SXXN','SNSXXN',
                 'SNSNSNSNSN','SNSEWNXXX','SNSNSNXXX']:
        print "'"+test+"'",':',dance.legal(test)
    
