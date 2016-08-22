import random


def get_split():
    probs = [0.8, 0.2]
    r = random.random()
    index = 0
    while(r >= 0 and index < len(probs)):
        r -= probs[index]
        index += 1

    if index - 1 == 0:
        return 'train'

    return 'test'
