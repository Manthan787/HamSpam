from Indexer import index
from Parser import BatchParser
import Feedback
from config import *


labels = Feedback.load_labels()
parser = BatchParser(DATA_PATH, labels)
parsed_docs = parser.parse()

index(parsed_docs)