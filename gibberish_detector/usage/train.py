import argparse

from .common import valid_file


def add_arguments(parent: argparse._SubParsersAction) -> None:
    parser = parent.add_parser(
        'train',
        help='Trains a model to be used for gibberish detection.',
        description=(
            'To identify if something is gibberish, a model must first be trained to teach '
            'the computer what is *not* gibberish. Then, anything not likely to be a real '
            'word would therefore be gibberish.'
        ),
    )

    parser.add_argument(
        'filename',
        nargs='+',
        help='Specifies the corpus files to be used for training the model.',
        type=valid_file,
    )

    parser.add_argument(
        '--amend',
        nargs=1,
        help='If specified, will improve existing model with new results.',
        type=valid_file,
    )
