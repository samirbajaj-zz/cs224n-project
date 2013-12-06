"""
CS 221/224N, Stanford University, Summer/Fall 2013
Author: Samir Bajaj (http://www.samirbajaj.com)

You are free to use all or any part of this code, as long as you acknowledge this
contribution by including a reference in your work. This is a student research
project, and no warranties of any kind are implied.
"""
from __future__ import division
from summarizer import Summarizer
from sentence import Sentence
from util import Util
import os
import heapq
import numpy as np
import networkx



class PageRank(Summarizer):
    """Random Surfer-based ranking of sentences."""

    def summarize(self, document_path):
        """
        Compute the PageRank of each sentence based on edge weights that are
        derived from the cosine similarity between sentences.
        """
        sentences = {} # key=index, value=sentence

        with open(document_path, 'r') as f:
            index = 0
            for line in f:
                s = Util.tokenize(line, Summarizer.non_space)
                sentence = []
                for w in s:
                    sentence.append(w)
                    if Summarizer.sentence_terminator.search(w):
                        sent = Sentence(sentence, Summarizer.punctuation, Summarizer.stopwords, Summarizer.stemmer)
                        sentences[index] = sent
                        sentence = []
                        index += 1

        # Now that we have the sentences, we need a lexicon so that we can compute
        # the cosine similarity between sentences.
        #
        lexicon = {}
        with open( os.path.join(Summarizer.BASE_DIR, 'LEXICON'), 'r') as f:
            word_counter = 0
            for line in f:
                count, word = line.split()
                lexicon[word] = word_counter
                word_counter += 1

        # Multi-dimensional vectors representing sentences in the space of words
        S = np.zeros(len(sentences) * len(lexicon), dtype=np.dtype('Float64')).reshape(len(sentences), len(lexicon))
        for i in range(len(sentences)):
            for w in sentences[i].stemmed:
                S[i, lexicon[w]] = 1

        P = np.dot(S, S.transpose()) # Numerator of the cosine similarity expression

        # Now zero out the diagonal elements (corresponds to removing self loops)
        P -= np.diag(np.diag(P))

        # calculate the denominator of the cosine similarity expression (i.e. the
        # normalization factor): this is the product of the magnitudes of the two
        # vectors whose dot product makes up the numerator
        #
        # we start with calculating the square root of the sum of the squares of
        # each vector's components
        D = np.reshape( np.sum(S**2, axis=1)**0.5, (len(S), 1) )
        # Now we compute the product of the square roots of the different vectors
        DD = np.dot(D, D.transpose())
        # element-wise division to get the similarity scores
        P = np.divide(P, DD)

        # At this point, P is essentially a weighted Adjacency matrix

        G = networkx.DiGraph(np.nan_to_num(P)) # Look up documentation of numpy.nan_to_num()
        pagerank = networkx.pagerank_numpy(G)

        important = heapq.nlargest(100, pagerank, key=lambda x: pagerank[x])
        #print [(x, pagerank[x]) for x in important]
        totalWords = 0
        selected = []
        already_included = set()

        for i in important:
            if sentences[i] not in already_included: # no duplicates
                already_included.add(sentences[i])
                selected.append((i, sentences[i]))
                totalWords += sentences[i].getLength()
                if totalWords > 100:
                    break

        # return the selected sentences in their order of appearance in the document
        return [s[1] for s in sorted(selected, key=lambda x: x[0])]