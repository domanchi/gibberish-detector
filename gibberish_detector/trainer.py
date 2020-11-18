import math
import string
from typing import Dict
from typing import Generator
from typing import Tuple


def train(filename: str, charset: str = string.ascii_letters) -> Dict[str, Dict[str, float]]:
    """
    Trains a normalized probability distribution table of ngrams of length 2, from the file
    content specified. Returned floats indicate the relative chance that a value is gibberish
    (lower value means more like known context).

    :returns: dictionary, so that it's easier to work with the raw model in the code.
         The caller will be responsible for handling appropriate serialization.
    """
    # TODO: make option for case insensitivity.

    # Assume that we have seen 10 of each character pair. This acts as a kind of prior /
    # smoothing factor. This way, if we see a character transition during live runs that
    # we've never observed in the past, we won't assume the entire string has 0 probability.
    counts = {
        key: {key: 10.0 for key in charset}
        for key in charset
    }

    iterator = NGramIterator(2, charset)
    with open(filename) as f:
        for line in f.readlines():
            for a, b in iterator.get(line):
                counts[a][b] += 1

    # Normalize the counts, so that they become log probabilities.
    # This helps avoid numeric underflow issues with long texts.
    # Justification:
    # http://squarecog.wordpress.com/2009/01/10/dealing-with-underflow-in-joint-probability-calculations/
    for row in counts.values():
        total = sum(row.values())
        for index, value in row.items():
            row[index] = - math.log(float(value) / total)

    return counts


class NGramIterator:
    def __init__(self, size: int, charset: str = string.ascii_letters) -> None:
        self.charset = set(charset)
        self.size = size

    def get(self, text: str) -> Generator[Tuple, None, None]:
        filtered = [c for c in text if c in self.charset]
        for start in range(0, len(filtered) - self.size + 1):
            yield tuple(filtered[start:start + self.size])
