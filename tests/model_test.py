import string

import pytest

from gibberish_detector.model import Model


class TestUpdate:
    @staticmethod
    def test_basic():
        with open('examples/quote.txt') as f:
            lines = f.readlines()

        # First, train two different models.
        modelA = Model(charset=string.ascii_letters)
        for line in lines[:int(len(lines) / 2)]:
            modelA.train(line)

        modelB = Model(charset=string.ascii_letters)
        for line in lines[int(len(lines) / 2):]:
            modelB.train(line)

        assert modelA['ay'] != modelB['ay']

        # Then, train a model that encompasses both data sets.
        modelC = Model(charset=string.ascii_letters)
        for line in lines:
            modelC.train(line)

        # Since modelA and modelB have both halves of the dataset, they should
        # be the same when combined.
        modelA.update(modelB)
        assert modelA['ay'] == modelC['ay']

    @staticmethod
    @pytest.mark.parametrize(
        'seedA, seedB',
        (
            ('ababab', 'acacac'),
            ('ababab', 'bcbcbc'),
            ('ababab', 'cdcdcd'),
        ),
    )
    def test_carries_over_charset(seedA, seedB):
        modelA = Model(charset=''.join(set(seedA)))
        modelA.train(seedA)

        with pytest.raises(KeyError):
            modelA[seedB[:2]]

        modelB = Model(charset=''.join(set(seedB)))
        modelB.train(seedB)
        modelA.update(modelB)

        # They should be the same frequencies.
        # NOTE: We don't use the normalized data set, since this could vary based
        # on the number of repeated elements between the two seeds.
        assert modelA.data[seedA[0]][
            seedA[1]
        ] == modelA.data[seedB[0]][seedB[1]]
