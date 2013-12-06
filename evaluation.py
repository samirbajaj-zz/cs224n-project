"""
CS 221/224N, Stanford University, Summer/Fall 2013
Author: Samir Bajaj (http://www.samirbajaj.com)

You are free to use all or any part of this code, as long as you acknowledge this
contribution by including a reference in your work. This is a student research
project, and no warranties of any kind are implied.
"""
from __future__ import division
from util import Util
from summarizer import Summarizer
from sentence import Sentence
import argparse


def unigrams(document_path):
    """Break sentences in a document into unigrams"""
    sentences = set()

    with open(document_path, 'r') as f:
        for line in f:
            s = Util.tokenize(line, Summarizer.non_space)
            sentence = []
            for w in s:
                sentence.append(w)
                if Summarizer.sentence_terminator.search(w):
                    sent = Sentence(sentence, Summarizer.punctuation, Summarizer.stopwords, Summarizer.stemmer)
                    sentences.add(sent)
                    sentence = []

    all_unigrams = set()
    for sentence in sentences:
        stemmed = sentence.stemmed
        for i in range(len(stemmed)):
            all_unigrams.add(stemmed[i])
    return all_unigrams


def trigrams(document_path):
    """Break sentences in a document into trigrams"""
    sentences = set()

    with open(document_path, 'r') as f:
        for line in f:
            s = Util.tokenize(line, Summarizer.non_space)
            sentence = []
            for w in s:
                sentence.append(w)
                if Summarizer.sentence_terminator.search(w):
                    sent = Sentence(sentence, Summarizer.punctuation, Summarizer.stopwords, Summarizer.stemmer)
                    sentences.add(sent)
                    sentence = []

    all_trigrams = set()
    for sentence in sentences:
        stemmed = sentence.stemmed
        for i in range(len(stemmed)-3):
            if i+2 < len(stemmed):
                all_trigrams.add((stemmed[i], stemmed[i+1], stemmed[i+2]))
    return all_trigrams


def main(args):
    if args['model'] == 3:
        gold = trigrams(args['gold'])
        test = trigrams(args['test'])
    else:
        gold = unigrams(args['gold'])
        test = unigrams(args['test'])
    common = gold.intersection(test)
    p = len(common)/len(test)
    r = len(common)/len(gold)
    f1 = 0
    if p+r > 0: f1 = 2*p*r/(p+r)
    print 'P:', p, 'R:', r, 'F1:', f1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluate a summary against a gold extract',
                                     epilog='Copyright (C) 2013 Samir Bajaj, http://www.samirbajaj.com')
    parser.add_argument('-gold', required=True, help='Path of the text file containing the gold summary')
    parser.add_argument('-test', required=True, help='Path of the text file containing the summary to be evaluated')
    parser.add_argument('-model', choices=[1, 3], default=3, type=int, help='Use unigrams or trigrams to compute precision and recall; default 3')
    args = parser.parse_args()
    main(args.__dict__)
