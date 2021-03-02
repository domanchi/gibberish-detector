import pytest

from gibberish_detector import serializer
from gibberish_detector.model import Model


@pytest.mark.parametrize(
    'line',
    (
        # Basic case
        'aaaaaaaaaa',

        # Nested with multiple values
        'aaaaaaaaab',

        # Multiple top level
        'aaaaabbbbb',
        'aabbaabbaa',
    ),
)
def test_success(line):
    model = Model('ab')
    model.train(line)
    assert model == serializer.deserialize(serializer.serialize(model))
