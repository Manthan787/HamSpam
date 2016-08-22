// Groovy script to fetch n-grams from elasticsearch
// In order for this script to work, elasticsearch shingles must be setup
// while creating the index.

def features = []
int gramSize = 1 // Change this value to get bi-grams or tri-grams

for(String term: doc['text'].values) {
    if(term.tokenize(" ").size() <= gramSize) {
      features.add(term);
    }
};
return features;
