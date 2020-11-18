import argparse

from .common import valid_file


def add_arguments(parent: argparse._SubParsersAction) -> None:
    parser = parent.add_parser(
        'detect',
        help='Uses a trained model to identify gibberish strings.',
    )

    parser.add_argument(
        '-m',
        '--model',
        required=True,
        type=valid_file,
        help='Filename for trained model.',
    )
    parser.add_argument(
        '-l',
        '--limit',
        default=4.0,
        type=float,
        help='Specifies the limit for strings to be considered gibberish.',
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--string',
        type=str,
        help='Check string to determine gibberish status.',
    )
    group.add_argument(
        '-i',
        '--interactive',
        action='store_true',
        help='Launches tool in interactive mode, to determine multiple words\' gibberish status.',
    )
