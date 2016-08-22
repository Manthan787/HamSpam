# HamSpam
Spam classifier for email using n-grams and skipgrams

Even though the project was built to perform classification on [this](http://plg.uwaterloo.ca/~gvcormac/treccorpus07/) dataset, it can be used for other datasets as well.


## Requirements
In order to run the code, please install following dependencies first:

[Elasticsearch](https://elasticsearch-py.readthedocs.io/en/master/)
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
[nltk](http://www.nltk.org/)
[scipy](https://www.scipy.org/)
[sklearn](http://scikit-learn.org/stable/)

or just run:

    pip install -r requirements.txt
  

## Features
The documents are first indexed in elasticsearch for efficient retrieval of n-grams and skipgrams. The dataset used had above 400k unigrams,
2M+ bigrams and 15M+ skipgrams (2-skip-bigrams).

Given the huge number of features, sparse matrix representation is used for document-term matrix.

## Results
The classification accuracy is above 99% for unigrams only, unigrams and bigrams & 2-skip-bigrams features for the given dataset using
LogisticRegression classifier.
