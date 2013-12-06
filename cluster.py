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
from sklearn.cluster import KMeans
import numpy as np



class Cluster(Summarizer):
    """KMeans-based clustering of sentences."""
    NUM_CLUSTERS = 20

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

        matrix = np.zeros((len(sentences), len(allwords)))
        for i, sent in enumerate(sentences):
            for t in sent.stemmed:
                matrix[i, allwords[t]] = Util.tfidf(t, self.tf, self.df, Summarizer.NUM_DOCS)

        # Normalize
        normalizer = np.reshape(np.sum(matrix**2, axis=1)**0.5, (len(matrix), 1))
        matrix /= normalizer

        model = KMeans(n_clusters=Cluster.NUM_CLUSTERS, tol=1e-9)
        model.fit_predict(np.nan_to_num(matrix))
        labels = model.labels_

        totalWords = 0
        selected = []

        # From each cluster, pick the sentence that is nearest to the cluster
        # centroid
        for i in range(Cluster.NUM_CLUSTERS):
            member_indices = np.where(labels == i)
            distances = np.dot(matrix[member_indices], model.cluster_centers_[i])
            closest_index = np.argmin(distances, 0)
            # 'closest_index' is the index into the member_indices array
            member_index = member_indices[0][closest_index]
            selected.append((member_index, sentences[member_index]))  # stash the index of the sentence as well
            totalWords += sentences[member_index].getLength()
            if totalWords > 100:
                break

        # return the selected sentences in their order of appearance in the document
        return [s[1] for s in sorted(selected, key=lambda x: x[0])]

