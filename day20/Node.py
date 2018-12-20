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
