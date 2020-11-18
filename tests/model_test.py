import string

from gibberish_detector.model import Model


def test_update():
    with open('examples/quote.txt') as f:
        lines = f.readlines()

    modelA = Model(charset=string.ascii_letters)
    for line in lines[:int(len(lines) / 2)]:
        modelA.train(line)

    modelB = Model(charset=string.ascii_letters)
    for line in lines[int(len(lines) / 2):]:
        modelB.train(line)

    assert modelA['ay'] != modelB['ay']

    modelC = Model(charset=string.ascii_letters)
    for line in lines:
        modelC.train(line)

    modelA.update(modelB)
    assert modelA['ay'] == modelC['ay']
