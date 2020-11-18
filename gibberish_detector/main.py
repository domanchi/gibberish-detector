import argparse
import sys
from typing import List
from typing import Optional

from . import serializer
from . import trainer
from .detector import Detector
from .exceptions import ParsingError
from .usage import parse_args


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    return {
        'train': _handle_train_action,
        'detect': _handle_detect_action,
    }[args.action](args)


def _handle_train_action(args: argparse.Namespace) -> int:
    model = None
    for filename in args.filename:      # pragma: no cover
        if not model:
            model = trainer.train(filename)
        else:
            model.update(trainer.train(filename))

    if not model:       # pragma: no cover
        # This should never happen, since we setup argparse to require filenames.
        # However, this conditional keeps mypy happy.
        return 1

    print(serializer.serialize(model))
    return 0


def _handle_detect_action(args: argparse.Namespace) -> int:
    try:
        with open(args.model) as f:
            model = serializer.deserialize(f.read())
    except IOError:     # pragma: no cover
        print(
            'error: There was an issue opening your model.',
            file=sys.stderr,
        )
        return 1
    except ParsingError:        # pragma: no cover
        print(
            'error: There was an issue parsing your model. Try re-creating it.',
            file=sys.stderr,
        )
        return 1

    detector = Detector(model, args.limit)
    if not args.interactive:
        print(detector.is_gibberish(args.string))
        return 0

    print('Entering interactive mode. Press ctrl+d to quit.')
    while True:
        try:
            text = input('Input text: ')
            print(
                '{:<5} ({})'.format(
                    'True' if detector.is_gibberish(text) else 'False',
                    round(detector.calculate_probability_of_being_gibberish(text), 3),
                ),
            )
        except EOFError:
            break
        except KeyboardInterrupt:
            # Let's be forgiving about following instructions
            break

    return 0
