import math
import string
from typing import Any
from typing import Dict

from .util import NGramIterator


SMOOTHING_FACTOR = 10.0


class Model:
    def __init__(self, charset: str):
        self.ngram_size = 2

        # Assume that we have seen 10 of each character pair. This acts as a kind of prior /
        # smoothing factor. This way, if we see a character transition during live runs that
        # we've never observed in the past, we won't assume the entire string has 0 probability.
        self.data = {
            key: {key: SMOOTHING_FACTOR for key in charset}
            for key in charset
        }

        self.charset = charset
        self.iterator = NGramIterator(self.ngram_size, charset)

    @classmethod
    def from_dict(cls, data: Dict[str, Dict[str, float]]) -> 'Model':
        """
        :param data: the `json()` representation for this model.
        """
        # TODO: customize charset
        model = cls(string.ascii_letters)
        model.data = {}
        for i, row in data.items():
            model.data[i] = {}

            for j, value in row.items():
                # reverse the log process
                model.data[i][j] = math.exp(-value)

        return model

    def train(self, line: str) -> None:
        for a, b in self.iterator.get(line):
            self.data[a][b] += 1

    def update(self, other: 'Model') -> None:
        """
        :param other: unnormalized model
        """
        for i, row in other.data.items():
            for j, value in row.items():
                self.data[i][j] += value - SMOOTHING_FACTOR

    def json(self) -> Dict[str, Dict[str, float]]:
        """
        This outputs a reversible representation for the model.
        Use this function for serialization, but the `normalize` function for detection.
        """
        # TODO: maybe this should be cached?
        output: Dict[str, Dict[str, float]] = {}
        for i, row in self.data.items():
            output[i] = {}
            for j, value in row.items():
                output[i][j] = - math.log(value)

        return output

    def normalize(self) -> Dict[str, Dict[str, float]]:
        # Normalize the counts, so that they become log probabilities.
        # This helps avoid numeric underflow issues with long texts.
        # Justification:
        # http://squarecog.wordpress.com/2009/01/10/dealing-with-underflow-in-joint-probability-calculations/
        output: Dict[str, Dict[str, float]] = {}
        for i, row in self.data.items():
            output[i] = {}
            total = sum(row.values())
            for j, value in row.items():
                output[i][j] = - math.log(float(value) / total)

        return output

    def __getitem__(self, key: str) -> float:
        if len(key) != self.ngram_size:
            raise KeyError('Invalid key!')

        return self.json()[key[0]][key[1]]

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Model):
            raise NotImplementedError

        return self.data == other.data
