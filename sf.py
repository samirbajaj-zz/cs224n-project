"""
CS 221/224N, Stanford University, Summer/Fall 2013
Author: Samir Bajaj (http://www.samirbajaj.com)

You are free to use all or any part of this code, as long as you acknowledge this
contribution by including a reference in your work. This is a student research
project, and no warranties of any kind are implied.
"""
from __future__ import division
from collections import defaultdict
from util import Util
from summarizer import Summarizer
from sentence import Sentence
import pickle
import sys


def main(argv):
    """Compute the sentence frequency of each term"""

    # How many sentences does each word appear in?
    lexicon = defaultdict(lambda: set())

    for arg in argv:
        with open(arg, 'r') as fin:
            sentences = list()
            for line in fin:
                s = Util.tokenize(line, Summarizer.non_space)
                sentence = []
                for w in s:
                    sentence.append(w)
                    if Summarizer.sentence_terminator.search(w):
                        sent = Sentence(sentence, Summarizer.punctuation, Summarizer.stopwords, Summarizer.stemmer)
                        sentences.append(sent)
                        sentence = []

            for sent in sentences:
                for w in sent.stemmed:
                    lexicon[w].add(sent) # set() will de-duplicate

        sf = {}
        for w in lexicon:
            sf[w] = len(lexicon[w])

        #print sf
        with open('sf.dat', 'wb') as out:
            pickle.dump(sf, out)


if __name__ == '__main__':
    main(sys.argv[1:])

