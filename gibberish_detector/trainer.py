import string

from .model import Model


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
    model = Model(charset)
    for line in content.splitlines():
        model.train(line)

    return model


if __name__ == '__main__':
    # Sample execution
    import json
    from gibberish_detector.util import get_path_to
    print(json.dumps(train(get_path_to('examples/big.txt')), indent=2))
