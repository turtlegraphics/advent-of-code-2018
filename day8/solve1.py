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
    meta = 0
    len = 2
    for c in range(children):
        (childlen, childmeta) = read_node(start+len,depth+1)
        len += childlen
        meta += childmeta
    for m in range(vals[start+1]):
        print '-'*depth,'meta',vals[start+len]
        meta += vals[start+len]
        len+=1
    return(len,meta)

print read_node(0,1)
