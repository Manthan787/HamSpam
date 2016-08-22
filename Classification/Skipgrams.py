from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
import itertools
from nltk import ngrams


def skipgrams(sequence, n, k):
    """
    :param sequence: a list of words/tokens
    :param n: length of each gram
    :param k: slop
    :return: Skipgrams fro the given sequence
    :example: "Insurgents killed in fight" with n=2, k=2 would yield
                 [("Insurgents", "killed"), ("Insurgents", "in"),
                 ("Insurgents", "fight"),("killed", "in"), ("killed", "fight")]
    """
    for ngram in ngrams(sequence, n + k, pad_right=True):
        head = ngram[:1]
        tail = ngram[1:]
        for skip_tail in itertools.combinations(tail, n - 1):
            if skip_tail[-1] is None:
                continue
            yield head + skip_tail


def find_skipgrams(text):
    """
        Finds skipgrams in a given string.
        For efficiency purposes, the skipgrams are only searched per sentence,
        as opposed to extending the chain to the entire text.
    """
    sent_tokens = sent_tokenize(text)
    tokenizer = RegexpTokenizer(r'\w+')
    grams = []
    for sent in sent_tokens:
        tokens = tokenizer.tokenize(sent)
        grams += skipgrams(tokens, 2, 2)

    return grams
