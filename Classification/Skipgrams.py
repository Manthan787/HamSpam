from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
import itertools
from nltk import ngrams


def skipgrams(sequence, n, k):
    for ngram in ngrams(sequence, n + k, pad_right=True):
        head = ngram[:1]
        tail = ngram[1:]
        for skip_tail in itertools.combinations(tail, n - 1):
            if skip_tail[-1] is None:
                continue
            yield head + skip_tail


def tokenize(text):
    sent_tokens = sent_tokenize(text)
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = []
    for sent in sent_tokens:
        tokens += tokenizer.tokenize(sent)

    return tokens


def find_skipgrams(text):
    tokens = tokenize(text)
    grams = skipgrams(tokens, 2, 2)

    return grams


