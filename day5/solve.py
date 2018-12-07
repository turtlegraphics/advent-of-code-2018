import sys
import string
import re

filename = 'input.txt'
if len(sys.argv) > 1:
    filename = sys.argv[1]

data = open(filename).read().strip()


def onepass(s):
    for c in string.ascii_lowercase:
        s = re.sub(c + c.upper(),'',s)
        s = re.sub(c.upper() + c,'',s)
    return s

def react(s):
    oldlen = len(s)
    s = onepass(s)
    while len(s) < oldlen:
        oldlen = len(s)
        s = onepass(s)
    return s

r = react(data)
print len(r)

for c in string.ascii_lowercase:
    k = re.sub('['+c+c.upper()+']','',r)
    print c, len(react(k))
