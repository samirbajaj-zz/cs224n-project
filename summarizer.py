"""
CS 221/224N, Stanford University, Summer/Fall 2013
Author: Samir Bajaj (http://www.samirbajaj.com)

You are free to use all or any part of this code, as long as you acknowledge this
contribution by including a reference in your work. This is a student research
project, and no warranties of any kind are implied.
"""
import abc
import re
import os
import porter
import pickle



class Summarizer(object):
    """Abstract base class for all summarizers."""

    NUM_DOCS = 37
    BASE_DIR = '/Users/samir/cs224n/project'
    stopwords = set( open( os.path.join(BASE_DIR, 'stop_words.txt'), 'r').read().strip().split(',') )
    word_re = re.compile('\w+') # drop trailing non-alphanumeric chars
    non_space = re.compile('\S+')
    non_alnum_ending = re.compile('\W$')
    punctuation = re.compile('[\-.,?!:;\'()&\[\]\$]')
    sentence_terminator = re.compile('[.?!]$')
    numbers = re.compile(r'[_\d.]+') # numbers and other strange tokens made up of underscores; re.compile(r'[\d.]*\d+')

    stemmer = porter.PorterStemmer()

    def __init__(self):
        self.df = None
        self.tf = {}

    # tf is the frequency of a word in the document being summarized;
    # df is its frequency in the document collection (all 37 plays)
    def initialize(self, tf_filename, df_filename):
        with open( os.path.join(Summarizer.BASE_DIR, df_filename), 'r') as f:
            self.df = pickle.load(f)

        with open(tf_filename, 'r') as f:
            for line in f:
                count, word = line.split()
                self.tf[word] = int(count)


    @abc.abstractmethod
    def summarize(self, document_path):
        return

