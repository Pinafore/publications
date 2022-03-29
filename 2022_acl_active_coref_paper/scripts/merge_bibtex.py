#!/usr/bin/python

import re
import sys
from collections import defaultdict

def read_bibtex(file):
    file = open(file).read()

    d = defaultdict(str)

    for ii in file.split("\n@"):
        record = ii.rsplit("}", 1)[0]

        try:
            id = record.split("\n")[0].split("{")[1]
            d[id.lower()] = "\n@%s\n}" % record.strip().replace("\t", "    ")
        except IndexError:
            None
    return d

if __name__ == "__main__":
    left, right = sys.argv[1:]

    left = read_bibtex(left)
    right = read_bibtex(right)

    indices = list(set(left) | set(right))
    indices.sort()

    for ii in indices:
        entry = left[ii]
        if len(right[ii]) > 0 and len(right[ii]) < len(left[ii]):
            entry = right[ii]

        print("%s\n" % entry.strip())
