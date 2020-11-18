import math
import string

from .types import Model
from .util import NGramIterator


def train(filename: str, charset: str = string.ascii_letters) -> Model:
    """
    Trains a normalized probability distribution table of ngrams of length 2, from the file
    content specified. Returned floats indicate the relative chance that a value is gibberish
    (lower value means more like known context).

    :returns: dictionary, so that it's easier to work with the raw model in the code.
         The caller will be responsible for handling appropriate serialization.
    :raises: IOError
    """
    with open(filename) as f:
        return train_on_content(f.read(), charset)


def train_on_content(content: str, charset: str) -> Model:
    # TODO: make option for case insensitivity.

    # Assume that we have seen 10 of each character pair. This acts as a kind of prior /
    # smoothing factor. This way, if we see a character transition during live runs that
    # we've never observed in the past, we won't assume the entire string has 0 probability.
    counts = {
        key: {key: 10.0 for key in charset}
        for key in charset
    }

    iterator = NGramIterator(2, charset)
    for line in content.splitlines():
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


if __name__ == '__main__':
    # Sample execution
    import json
    from gibberish_detector.util import get_path_to
    print(json.dumps(train(get_path_to('examples/big.txt')), indent=2))
