from elasticsearch import Elasticsearch
from config import *
import sys
from os.path import join
from Skipgrams import find_skipgrams


es = Elasticsearch(timeout=1000)


def extract():
    features = []

    page = es.search(index=INDEX,
                     doc_type=TYPE,
                     scroll='2m', size=10000, body=FEATURES_BODY)

    sid = page['_scroll_id']
    scrollSize = page['hits']['total']
    size = 0

    while scrollSize > 0:
        hits = page['hits']['hits']
        for hit in hits:
            if 'fields' in hit:
                features += hit['fields']['unigrams']
        scrollSize = len(hits)
        size += scrollSize
        sys.stdout.write("scrolled through %d links... \r" % (size))
        sys.stdout.flush()
        sid = page['_scroll_id']
        page = es.scroll(scroll_id=sid, scroll='2m')

    return features


def extract_skipgrams():
    print "Extracting skipgrams ..."
    features = []

    page = es.search(index=INDEX,
                     doc_type=TYPE,
                     scroll='2m', size=10000)

    sid = page['_scroll_id']
    scrollSize = page['hits']['total']
    size = 0

    while scrollSize > 0:
        hits = page['hits']['hits']
        for hit in hits:
            text = hit['_source']['text']
            features += find_skipgrams(text)
        scrollSize = len(hits)
        size += scrollSize
        sys.stdout.write("scrolled through %d links... \r" % (size))
        sys.stdout.flush()
        sid = page['_scroll_id']
        page = es.scroll(scroll_id=sid, scroll='2m')
        write_skipgrams(features, 'skipgrams')
        features = []


def write_features(features, filename):
    file_path = join(SPLIT_PATH, filename)
    string = ''
    for i, feature in enumerate(set(features)):
        string += "{}\n".format(feature.encode('utf-8', 'ignore'))
        sys.stdout.write("Appended %d Features \r" %i)
        sys.stdout.flush()

    with open(file_path, 'a') as f:
        f.write(string)


def write_skipgrams(features, filename):
    file_path = join(SPLIT_PATH, filename)
    string = ''
    for i, feature in enumerate(set(features)):
        feature = ' '.join(feature)
        string += "{}\n".format(feature.encode('utf-8', 'ignore'))
        sys.stdout.write("Appended %d Features \r" %i)
        sys.stdout.flush()

    with open(file_path, 'a') as f:
        f.write(string)



if __name__ == '__main__':
    features = extract_skipgrams()