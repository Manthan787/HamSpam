def features = []

for(String term: doc['text'].values) {
    if(term.tokenize(" ").size() == 1) {
      features.add(term);
    }
};
return features;
