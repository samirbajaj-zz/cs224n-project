"""
CS 221/224N, Stanford University, Summer/Fall 2013
Author: Samir Bajaj (http://www.samirbajaj.com)

You are free to use all or any part of this code, as long as you acknowledge this
contribution by including a reference in your work. This is a student research
project, and no warranties of any kind are implied.
"""
from __future__ import division
import math
import random
import numpy as np


class Util(object):
    """Utility methods"""
    @staticmethod
    def tokenize(text, word_re, splitter = None):
        if text is None or len(text) == 0: return []
        if splitter is None: return [word_re.search(w).group(0) for w in text.split() if word_re.search(w)]
        return [word_re.search(w).group(0) for w in text.split(splitter) if word_re.search(w)]

    @staticmethod
    def filter(regex, text):
        return [w for w in text if not regex.match(w)]

    @staticmethod
    def tfidf(word, tf, df, num_docs):
        return tf[word] * math.log(num_docs/df[word])



