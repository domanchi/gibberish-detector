import string

from . import serializer
from .model import Model
from .util import NGramIterator


def create_from_model(filename: str, limit: float = 4.0):
    """
    :raises: IOError
    :raises: ParsingError
    """
    with open(filename) as f:
        model = serializer.deserialize(f.read())

    return Detector(model, limit)


class Detector:
    def __init__(self, model: Model, threshold: float) -> None:
        self.model = model.normalize()
        self.limit = threshold

        # TODO: allow specification of charset
        self.iterator = NGramIterator(2, charset=string.ascii_letters)

    def is_gibberish(self, payload: str) -> bool:
        return self.calculate_probability_of_being_gibberish(payload) > self.limit

    def calculate_probability_of_being_gibberish(self, payload: str) -> float:
        """The higher the number, the more likely to be gibberish."""
        ngrams = list(self.iterator.get(payload))
        return sum([self.model[a][b] for a, b in ngrams]) / len(ngrams)
