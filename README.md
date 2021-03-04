[![PyPI version](https://badge.fury.io/py/gibberish-detector.svg)](https://badge.fury.io/py/gibberish-detector)

# Gibberish Detector

This is based off https://github.com/rrenaud/Gibberish-Detector, and adapted so that it is a
Python3 module.

## Examples

**Quickstart**:

```bash
$ gibberish-detector train examples/big.txt > big.model
$ gibberish-detector detect --model big.model --string "ertrjiloifdfyyoiu"
True
```

**Training Large Corpuses**:

```bash
$ gibberish-detector train $(ls examples) > generic.model
```

**Interactive Detection**:

```bash
$ gibberish-detector detect --model big.model --interactive
Entering interactive mode. Press ctrl+d to quit.
Input text: superman
False (2.375)
Input text: ertrjiloifdfyyoiu
True  (4.154)
```

## Installation

```
pip install gibberish-detector
```

## Usage

```
$ gibberish-detector -h
usage: gibberish-detector [-h] [--version] {train,detect} ...

positional arguments:
  {train,detect}
    train         Trains a model to be used for gibberish detection.
    detect        Uses a trained model to identify gibberish strings.

optional arguments:
  -h, --help      show this help message and exit
  --version       Display version information.
```

You can also use this as an imported module:

```python
>>> from gibberish_detector import detector
>>> Detector = detector.create_from_model('big.model')
>>> print(Detector.is_gibberish('ertrjiloifdfyyoiu'))
True
```
