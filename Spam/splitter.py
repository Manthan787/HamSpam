import random
from config import TRAIN_PORTION, TEST_PORTION


def get_split():
    """
        Randomly assigns "train" or "test" label to the document.
        Used while indexing to assign split to documents
        TRAIN_PORTION = 0.8 and TEST_PORTION = 0.2 (80% training & 20% training)
        Values can be changed for different TRAIN-TEST configurations
    """
    probs = [TRAIN_PORTION, TEST_PORTION]
    r = random.random()
    index = 0
    while(r >= 0 and index < len(probs)):
        r -= probs[index]
        index += 1

    if index - 1 == 0:
        return 'train'

    return 'test'
