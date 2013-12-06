"""
CS 221/224N, Stanford University, Summer/Fall 2013
Author: Samir Bajaj (http://www.samirbajaj.com)

You are free to use all or any part of this code, as long as you acknowledge this
contribution by including a reference in your work. This is a student research
project, and no warranties of any kind are implied.
"""
from __future__ import division
from tfidf import TfIdf
from cluster import Cluster
from svd import SVD
from pagerank import PageRank
import argparse


            
def main(args):
    summarizer = {
      'tfidf': TfIdf(),
      'cluster': Cluster(),
      'svd': SVD(),
      'pagerank': PageRank()
    }[args['alg']]

    summarizer.initialize(args['tf'], args['df'])
    summary = summarizer.summarize(args['doc'])

    for s in summary:
        print s,



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Summarize a text document',
                                     epilog='Copyright (C) 2013 Samir Bajaj, http://www.samirbajaj.com')
    parser.add_argument('-doc', required=True, help='The document to summarize')
    parser.add_argument('-alg', required=True, choices=['tfidf', 'cluster', 'svd', 'pagerank'], help='The algorithm to use')
    parser.add_argument('-tf', required=True, help='Path to the text file containing term frequencies')
    parser.add_argument('-df', help='Name of the pickle file containing document frequencies')
    args = parser.parse_args()
    main(args.__dict__)
