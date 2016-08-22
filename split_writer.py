from elasticsearch import Elasticsearch
from Spam.Feedback import load_labels
from config import *


es = Elasticsearch(timeout=1000)


def write_split_to_file(split):
    """
        Fetches all the documents for the given split ("train" or "test") from
        Elasticsearch and writes them to file.
    """
    ALL_DOCS = '''
        {{
          "size": 62000,
          "query": {{
            "match": {{
              "split": "{split}"
            }}
          }}
        }}
    '''.format(split=split)
    res = es.search(index='spam', doc_type='email', body=ALL_DOCS)
    hits = res['hits']['hits']
    string = ''
    for hit in hits:
        string += '{}\n'.format(hit['_id'])

    with open(SPLIT_PATH+split, 'w') as f:
        f.write(string)


if __name__ == '__main__':
    write_split_to_file('train')
    write_split_to_file('test')
