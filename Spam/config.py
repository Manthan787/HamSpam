DATA_PATH = '/Users/admin/Documents/CS6200/trec07p/data'
FEEDBACK_PATH = '/Users/admin/Documents/CS6200/trec07p/full/index'
# SPLITTER Config
TRAIN_PORTION = 0.8
TEST_PORTION = 0.2

# Elastic search config
INDEX = 'spam'
TYPE  = 'email'
ES_SETTINGS = """{
  "settings": {
    "index": {
      "store": {
        "type": "default"
      },
      "max_result_window": 85000,
      "number_of_shards": 1,
      "number_of_replicas": 1
    },
    "analysis": {
      "analyzer": {
        "my_english": {
          "type": "custom",
          "tokenizer": "standard",
          "stopwords_path": "stoplist.txt",
          "filter": [
            "standard",
            "lowercase",
            "custom_shingle"
          ]
        }
      },
      "filter": {
        "custom_shingle": {
            "type": "shingle",
            "min_shingle_size": "2",
            "max_shingle_size": "3"
        }
      }
    }
  },
  "mappings": {
    "email": {
      "properties": {
        "docno": {
          "type": "string",
          "store": true,
          "index": "not_analyzed"
        },
        "text": {
          "type": "string",
          "store": true,
          "index": "analyzed",
          "term_vector": "with_positions_offsets_payloads",
          "analyzer": "my_english"
        },
        "label": {
          "type": "string",
          "store": true,
          "index": "not_analyzed"
        },
        "split": {
          "type": "string",
          "store": true,
          "index": "not_analyzed"
        }
      }
    }
  }
}"""
