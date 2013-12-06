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
import numpy as np



class SVD(Summarizer):
    """SVD-based ranking of sentences."""

    def summarize(self, document_path):
        allwords = {}
        sentences = []

        with open(document_path, 'r') as f:
            index = 0
            for line in f:
                s = Util.tokenize(line, Summarizer.non_space)
                sentence = []
                for w in s:
                    sentence.append(w)
                    if Summarizer.sentence_terminator.search(w):
                        sent = Sentence(sentence, Summarizer.punctuation, Summarizer.stopwords, Summarizer.stemmer)
                        sentences.append(sent)
                        for t in sent.stemmed:
                            if t not in allwords:
                                allwords[t] = index
                                index += 1
                        sentence = []

        matrix = np.zeros((len(allwords), len(sentences)))
        for i, sent in enumerate(sentences):
            for t in sent.stemmed:
                matrix[allwords[t], i] = Util.tfidf(t, self.tf, self.df, Summarizer.NUM_DOCS)

        U, sigma, V_T = np.linalg.svd(matrix, full_matrices=False) # V is already transposed

        # The rows of V_T correspond to 'independent topics', and the columns are the sentences.
        # For each topic, we pick the sentence that has the highest strength (value) in the row.
        max_cols = V_T.argmax(axis=1)

        already_included = set()
        totalWords = 0
        selected = []

        for i in max_cols:
            if i not in already_included:
                already_included.add(i)
                selected.append((i, sentences[i])) # stash the index of the sentence as well
                totalWords += sentences[i].getLength()
                if totalWords > 100:
                    break

        # return the selected sentences in their order of appearance in the document
        return [s[1] for s in sorted(selected, key=lambda x: x[0])]
