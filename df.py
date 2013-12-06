"""
CS 221/224N, Stanford University, Summer/Fall 2013
Author: Samir Bajaj (http://www.samirbajaj.com)

You are free to use all or any part of this code, as long as you acknowledge this
contribution by including a reference in your work. This is a student research
project, and no warranties of any kind are implied.
"""
from __future__ import division
from collections import defaultdict
import pickle
import sys


def main(argv):
    """Compute the document frequency of each term"""
    lexicon = defaultdict(lambda: set())
    for arg in argv:
        with open(arg, 'r') as fin:
            for line in fin:
                count, word = line.split()
                lexicon[word].add(arg) # set() will de-duplicate

        
    df = {}
    for w in lexicon:
        df[w] = len(lexicon[w])

    #print df
    with open('df.dat', 'wb') as out:
        pickle.dump(df, out)


if __name__ == '__main__':
    main(sys.argv[1:])
