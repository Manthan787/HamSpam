from config import *
from elasticsearch import Elasticsearch
from sklearn import linear_model
from scipy.sparse import coo_matrix
import sys
import numpy as np
from os.path import join
from ..Spam import Feedback


es = Elasticsearch(timeout=1000)


def get_features():
    """
    :return: Features from the path SPAM_WORDS_PATH, Features' forward and reverse
             mapping to create sparse matrix and identify feature name from feature id
    """
    print "Getting features!"
    with open(SPAM_WORDS_PATH, 'r') as f:
        lines = f.readlines()

    features = []
    i = 0
    features_map = {}
    reverse_features_map = {}
    for line in lines:
        feature = line.strip().lower()
        features_map[feature] = i
        reverse_features_map[i] = feature
        i += 1
        features.append(feature)
    print len(features)
    return features, features_map, reverse_features_map


def get_doc_term_matrix(features_map, split="train", with_labels=True):
    """
    :param features_map: a dictionary with feature name as key and it's unique ID as value
    :param split: name of the split from where to get the document IDs for the matrix
    :param with_labels: True if labels for the Documents are also to be returned along
                        with feature representation
    :return: a dictionary containing terms and their TF for values in tokens in the
             feature vector for each document and labels for all those documents
    """
    doc_term = {}
    labels = {}
    i = 0
    all_docs = get_docs(split)
    feedback = Feedback.load_labels()
    for i, doc in enumerate(all_docs):
        res = es.termvectors(index=INDEX, doc_type=TYPE, id=doc)
        term_vectors = res['term_vectors']
        if len(term_vectors) > 0:
            terms = term_vectors['text']['terms']
            for term, values in terms.iteritems():
                if term in features_map:
                    doc_term.setdefault(doc, {}).setdefault(features_map[term], values['term_freq'])
        if with_labels:
            labels[doc] = str_to_int(feedback[doc])
        sys.stdout.write("Emails Processed: %d \r" %i)
        sys.stdout.flush()

    print len(labels)
    return doc_term, labels


def str_to_int(label):
    """
    :param label: Label "spam" or "ham"
    :return: 1 if label is "spam", 0 if label is "ham"
    """
    if label == 'spam':
        return 1

    return 0


def get_docs(split):
    """
    :param split: name of the split "train" or "test"
    :return: a list of document IDs in the given split
    """
    file_path = join(SPLIT_PATH, split)
    with open(file_path, 'r') as f:
        lines = f.readlines()

    docs = []
    for line in lines:
        docs.append(line.strip())

    return docs


def create_sparse_matrix(doc_term_matrix, labels, num_features, with_labels=True):
    """
    :param doc_term_matrix: Document-Term matrix as a dictionary with all the documents
                            containing TF counts for features that exist in them
                            exmaple,
                            {'doc1':
                                {'free': 3,
                                'dollar': 5}
                            }
    :param labels: Correspoiding labels for each of the documents
    :param num_features: number of total features
    :param with_labels: True if a list of corresponding labels for all the sparse matrix rows (documents)
                        is to be returned
    :return: scipy.sparse matrix, a list of corresponding labels and document map
    """
    doc_id = 0
    rows = []
    cols = []
    data = []
    Y = []
    doc_map = {}
    for doc, values in doc_term_matrix.iteritems():
        doc_map[doc_id] = doc
        for feature_id, tf in values.iteritems():
            rows.append(doc_id)
            cols.append(feature_id)
            data.append(tf)
        Y.append(labels[doc])
        doc_id += 1

    if with_labels:
        for email, label in labels.iteritems():
            if email not in doc_term_matrix:
                Y.append(label)

    rows = np.array(rows)
    cols = np.array(cols)
    data = np.array(data)
    matrix = coo_matrix((data, (rows, cols)), shape=(len(labels), num_features))
    return matrix, Y, doc_map


def train(X, Y):
    """
    :param X: Feature matrix
    :param Y: Labels
    :return: Model trained on Logistic Regression
    """
    model = linear_model.LogisticRegression()
    model = model.fit(X, Y)
    return model


def get_top_docs(probs, doc_map):
    labels = Feedback.load_labels()
    string = ''
    doc_score = {}
    for i, prob in enumerate(probs):
        if i in doc_map:
            doc_score[doc_map[i]] = prob

    sorted_docs = sorted(doc_score.items(), key=lambda x: x[0],reverse=True)

    for doc in sorted_docs:
        string += '{} {} {}\n'.format(doc, doc_score[doc], labels[doc])

    with open(join(SPLIT_PATH, 'top_docs'), 'w') as f:
        f.write(string)


def write_features_to_file(doc_term_matrix, labels, filename):
    """ Writes features to file in LibLinear sparse format"""
    doc_id = 0
    doc_map = {}
    string = ''
    for doc, values in doc_term_matrix.iteritems():
        doc_map[doc_id] = doc
        string += "{} ".format(labels[doc])
        sorted_values = sorted(values, key=lambda x: x)
        for value in sorted_values:
            string += "{}:{} ".format(value, values[value])
        string += "\n"
        # Y.append(labels[doc])
        doc_id += 1

    for email, label in labels.iteritems():
        if email not in doc_term_matrix:
            string += "{}".format(label)
            string += "\n"

    with open(filename, 'w') as f:
        f.write(string)


if __name__ == '__main__':
    features, features_map, reverse_features_map = get_features()
    doc_term_matrix, labels = get_doc_term_matrix(features_map)
    matrix, Y, _ = create_sparse_matrix(doc_term_matrix, labels, len(features))
    classifier = train(matrix, Y)

    doc_term_matrix, test_labels = get_doc_term_matrix(features_map, split="test")
    test_X, test_Y, doc_map = create_sparse_matrix(doc_term_matrix, test_labels, len(features))
    print classifier.score(test_X, test_Y)
