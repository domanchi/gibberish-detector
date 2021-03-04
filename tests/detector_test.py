import string

import pytest

from gibberish_detector import trainer
from gibberish_detector.detector import Detector


def test_calculate_probability_of_being_gibberish(model):
    detector = Detector(model, 2)

    assert (
        detector.calculate_probability_of_being_gibberish('quick') <
        detector.calculate_probability_of_being_gibberish('blah')
    )


def test_handles_values_outside_of_character_map_gracefully(model):
    detector = Detector(model, 4)

    assert not detector.is_gibberish('Quick')


@pytest.fixture
def model():
    return trainer.train_on_content(
        'the quick brown fox jumps over the lazy dog',
        string.ascii_lowercase,
    )
