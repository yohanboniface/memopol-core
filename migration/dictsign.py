#!/usr/bin/python

import anyjson
import sys
import difflib


def explore(o, depth=0, maxdepth=sys.maxint):
    if depth >= maxdepth:
        return
    t = type(o)
    if t == list or t == tuple:
        yield "L"
        for i in o:
            for ie in explore(i):
                yield ie
    elif t == dict:
        yield "D"
        keys = o.keys()
        keys.sort()
        for k in keys:
            yield k
            for ek in explore(o[k]):
                yield ek

def diffsig(left, right):
    print left
    print right
    g = difflib.unified_diff(left, right)
    for d in g:
        print d
    



def main():
    alldata = open(sys.argv[1], "r").read()
    root = anyjson.deserialize(alldata)
    signs = []
    for item in root[123:125]:
        print item["_id"]
        signs.append( [ x for x in explore(item, maxdepth=1) ])
    diffsig(signs[0], signs[1])    
    
    

if __name__ == "__main__":
    main()
