import sys

filename = 'input.txt'
if len(sys.argv) > 1:
    filename = sys.argv[1]

data = open(filename).read().strip()

vals = [int(v) for v in data.split()]

print vals

def read_node(start,depth):
    print '-'*depth,'child at',start
    children = vals[start]
    childvals = {}
    len = 2
    for c in range(children):
        (childlen, childval) = read_node(start+len,depth+1)
        len += childlen
        childvals[c] = childval
    print '-'*depth,'children vals',childvals
    
    if children == 0:
        meta = 0
        for m in range(vals[start+1]):
            meta += vals[start+len]
            len+=1
        print '-'*depth,'no children, meta=',meta
        return(len,meta)

    # has children
    meta = 0
    for m in range(vals[start+1]):
        child = vals[start+len]-1
        try:
            meta += childvals[child]
            print '-'*depth,'child',child,':',childvals[child]
        except:
            print '-'*depth,'child',child,'bad ref'
        len += 1

    print '-'*depth,children,'children, meta=',meta
    return(len,meta)
    
print read_node(0,1)
