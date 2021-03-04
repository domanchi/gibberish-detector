import math
from typing import Any
from typing import cast
from typing import Dict
from typing import Optional
from typing import Union

from .util import NGramIterator


# Assume that we have seen 10 of each character pair. This acts as a kind of prior /
# smoothing factor. This way, if we see a character transition during live runs that
# we've never observed in the past, we won't assume the entire string has 0 probability.
SMOOTHING_FACTOR = 10


class Model:
    def __init__(self, charset: str, ngram_size: int = 2):
        self.ngram_size = ngram_size

        self.data = {
            key: {key: SMOOTHING_FACTOR for key in charset}
            for key in charset
        }

        self.charset = charset
        self.iterator = NGramIterator(self.ngram_size, charset)

        self._normalized_model: Optional[Dict[str, Dict[str, float]]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, int, Dict[str, int]]]) -> 'Model':
        """
        :param data: the `json()` representation for this model.
        """
        model = cls(
            cast(str, data['charset']),
            int(cast(str, data.get('ngram_size', 2))),
        )
        model.data = cast(Dict[str, Dict[str, int]], data['counts'])

        return model

    def train(self, line: str) -> None:
        for a, b in self.iterator.get(line):
            self.data[a][b] += 1

        # reset cache
        self._normalized_model = None

    def update(self, other: 'Model') -> None:
        """
        This carries over the other model's charset, and unions it with the current one.
        This is because learning more about the "world" is not a bad thing: a more intelligent
        model is always better.

        :param other: unnormalized model
        """
        for i, row in other.data.items():
            if i not in self.data:
                self.data[i] = row
                continue

            for j, value in row.items():
                if j in self.data[i]:
                    # NOTE: We subtract the SMOOTHING_FACTOR here, since at this point,
                    # we're adding it twice (since it initializes the model).
                    self.data[i][j] += value - SMOOTHING_FACTOR
                else:
                    # However, if it's the first time we're seeing this pair, we keep
                    # the SMOOTHING_FACTOR.
                    self.data[i][j] = value

        # reset cache
        self.charset = ''.join(set(self.charset) | set(other.charset))
        self._normalized_model = None

    def json(self) -> Dict[str, Union[str, int, Dict[str, Dict[str, int]]]]:
        """
        This outputs a reversible representation for the model.
        Use this function for serialization, but the `normalize` function for detection.
        """
        return {
            'charset': self.charset,
            'ngram_size': self.ngram_size,
            'counts': self.data,
        }

    def normalize(self) -> Dict[str, Dict[str, float]]:
        """
        Models need to be normalized (converted into log probabilities), before using
        them to calculate probabilities, to avoid numeric underflow issues with long texts.

        See http://squarecog.wordpress.com/2009/01/10/dealing-with-underflow-in-joint-probability-calculations/     # noqa: E501
        for more information.
        """
        if self._normalized_model:
            return self._normalized_model

        output: Dict[str, Dict[str, float]] = {}
        for i, row in self.data.items():
            output[i] = {}
            total = sum(row.values())
            for j, value in row.items():
                # By dividing it by the total (hence, normalizing it), we essentially remove
                # the effects of the smoothing factor.
                output[i][j] = - math.log(float(value) / total)

        self._normalized_model = output
        return output

    def __getitem__(self, key: str) -> float:
        if len(key) != self.ngram_size:
            raise KeyError('Invalid key!')

        return self.normalize()[key[0]][key[1]]

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Model):
            raise NotImplementedError

        return self.data == other.data
