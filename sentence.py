"""
CS 221/224N, Stanford University, Summer/Fall 2013
Author: Samir Bajaj (http://www.samirbajaj.com)

You are free to use all or any part of this code, as long as you acknowledge this
contribution by including a reference in your work. This is a student research
project, and no warranties of any kind are implied.
"""
from __future__ import division
from util import Util



class Sentence:
    def __init__(self, words, punctuation_re, stopwords, stemmer):
        self.length = len(words)
        self.sentence = ' '.join(words)
        self.words = [w.lower() for w in words if not w.lower() in stopwords]
        self.tokens = [punctuation_re.sub(' ', w).strip() for w in self.words]
        self.stemmed = [stemmer.stem(t, 0, len(t)-1) for t in (' '.join(self.tokens)).split() if t not in stopwords]
        self.score = 0

    def __str__(self):
        return self.sentence

    def __hash__(self):
        hash = 31
        for w in self.stemmed:
            hash = hash * 101 + w.__hash__()
        return hash

    def __eq__(x, y):
        return cmp(x.stemmed, y.stemmed) == 0

    def getLength(self):
        return self.length

    def tfidf(self, tf, df, num_docs):
        if len(self.stemmed) == 0:
            return 0
        if not self.score == 0:
            return self.score
        for s in self.stemmed:
            self.score += Util.tfidf(s, tf, df, num_docs)
        return self.score