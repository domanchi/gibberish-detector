import pytest

from gibberish_detector import serializer
from gibberish_detector.model import Model


@pytest.mark.parametrize(
    'model',
    (
        # Basic case
        {
            'a': {'a': 2.0},
        },

        # Nested with multiple values
        {
            'a': {'a': 1.1, 'b': 1.2},
        },

        # Multiple top level
        {
            'a': {'a': 2.0},
            'b': {'b': 2.0},
        },
        {
            'a': {'a': 1.1, 'b': 1.2},
            'b': {'a': 0.9, 'b': 1.4},
        },
    ),
)
def test_success(model):
    model = Model.from_dict(model)
    assert model == serializer.deserialize(serializer.serialize(model))
