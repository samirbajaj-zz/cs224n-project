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



class TfIdf(Summarizer):
    """TF-IDF-based ranking of sentences."""

    def summarize(self, document_path):
        sentences = {}
        counter = 0

        with open(document_path, 'r') as f:
            for line in f:
                s = Util.tokenize(line, Summarizer.non_space)
                sentence = []
                for w in s:
                    sentence.append(w)
                    if Summarizer.sentence_terminator.search(w):
                        sent = Sentence(sentence, Summarizer.punctuation, Summarizer.stopwords, Summarizer.stemmer)
                        sentences[sent] = (sent.tfidf(self.tf, self.df, Summarizer.NUM_DOCS), counter)
                        sentence = []
                        counter += 1

        totalWords = 0
        selected = []
        already_included = set()
        # Use the tf-idf score to sort the sentences
        for sent in sorted(sentences, key=lambda x: sentences[x][0], reverse=True):
            if sent not in already_included: # no duplicates
                already_included.add(sent)
                selected.append(sent)
                totalWords += sent.getLength()
                if totalWords > 100:
                    break

        # return the selected sentences in their order of appearance in the document
        return sorted(selected, key=lambda x: sentences[x][1])