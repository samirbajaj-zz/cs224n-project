"""
An implementation of a Content-Based Filtering recommender system. This program
takes three files as input: Facebook profile data in XML, metadata for the TV
shows, and a list of stopwords. Note that the metadata and Facebook profile data
should have already been run through the stemmer before being presented to this 
program. A Porter stemmer is available in porter.py.

Warning: This program takes a very long time to run.

CS 229, Stanford University, Fall 2012
Author: Samir Bajaj (http://www.samirbajaj.com)

You are free to use all or any part of this code, as long as you acknowledge this
contribution by including a reference in your work. This is a student research
project, and no warrantees of any kind are implied.
"""
from __future__ import division
import re
import sys
import math
import random
import numpy as np
import xml.etree.ElementTree as ET


def tokenize(text, word_re, splitter = None):
    if text is None or text == 'N/A': return []
    if splitter is None: return [word_re.search(w).group(0) for w in text.split() if word_re.search(w)]
    return [word_re.search(w).group(0) for w in text.split(splitter) if word_re.search(w)]

def normalize(tvShows):
    if len(tvShows) == 0: return []
    return [show.strip().lower() for show in tvShows]

def encode(text):
    if len(text) == 0: return []
    return [w.encode('utf-8') for w in text]
    
def removeStopWords(text, stopwords):
    return [w for w in text if not w in stopwords]

def filter(regex, text):
    return [w for w in text if not regex.match(w)]

def sample(all, fraction):
    return random.sample(all, int(math.ceil(fraction * len(all))))

def createUserVector(user_words, all_words, vocabulary, vocab_size, idf):
    result = [0] * vocab_size
    for w in user_words:
        result[ vocabulary[w] ] += 1
    for i in range(len(result)):
        if result[i] == 0: continue
        result[i] = result[i] * idf[all_words[i]]
    return result
'''
def cosine(a, b):
    if len(a) != len(b):
        raise ValueError, "a and b must be same length"
    numerator = 0
    denoma = 0
    denomb = 0
    for i in range(len(a)):
        ai = a[i]             #only calculate once
        bi = b[i]
        numerator += ai*bi    #faster than exponent (barely)
        denoma += ai*ai
        denomb += bi*bi
    result = 1 - numerator / (math.sqrt(denoma * denomb))
    return result
'''

def cosine(u1, u2):
    norm1 = np.linalg.norm(u1)
    norm2 = np.linalg.norm(u2)
    return np.dot(u1, u2) / ( norm1 * norm2 )

def main(argv):
    if len(argv) > 1:
        print "Usage: Recommender.py <fbDataFile.xml>"
        sys.exit(0)
    stopwords = set( open('/Users/samir_bajaj/cs221/project/stop_words.txt', 'r').read().strip().split(',') )
    word_re = re.compile('\w+') # drop trailing non-alphanumeric chars
    numbers = re.compile(r'[_\d.]+') # numbers and other strange tokens made up of underscores; re.compile(r'[\d.]*\d+')
    with open(argv[0], 'r') as f:
        for line in f:
            s = tokenize(line, word_re)
            for w in s:
                if not w in stopwords: print w,

if __name__ == '__main__':
    main(sys.argv[1:])
