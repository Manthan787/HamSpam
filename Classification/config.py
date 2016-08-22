SPAM_WORDS_PATH = '/Users/admin/Documents/CS6200/HW7/skipgrams'
SPLIT_PATH = '/Users/admin/Documents/CS6200/HW7/'
INDEX = 'spam'
TYPE  = 'email'
CRAWL_INDEX = '1512_great_mordenist_artist'
CRAWL_TYPE = 'document'
CRAWL_TF_BODY = '''{{
"min_score": 1,
"query": {{
        "function_score": {{
          "functions": [
            {{
              "script_score": {{
                "script": {{
                  "inline": "_index[field][term].tf()",
                  "params": {{
                    "field": "TEXT",
                    "term": "{term}"
                  }}
                }}
              }}
            }}
          ],
          "boost_mode": "replace"
        }}
      }}
    }}
'''
TF_BODY = '''{{
"min_score": 1,
  "query": {{
    "filtered": {{
      "query": {{
        "function_score": {{
          "functions": [
            {{
              "script_score": {{
                "script": {{
                  "inline": "_index[field][term].tf()",
                  "params": {{
                    "field": "text",
                    "term": "{term}"
                  }}
                }}
              }}
            }}
          ],
          "boost_mode": "replace"
        }}
      }},
      "filter": {{
        "term": {{
          "split": "{split}"
        }}
      }}
    }}
  }}
}}
'''

FEATURES_BODY = '''
{
  "script_fields": {
    "unigrams": {
      "script": {
        "lang": "groovy",
        "file": "extractFeatures"
      }
    }
  }
}
'''



