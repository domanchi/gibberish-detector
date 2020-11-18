import argparse
from typing import List
from typing import Optional

from . import detect
from . import train
from ..__version__ import VERSION


def parse_args(argv: Optional[List[str]]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--version',
        action='version',
        version=VERSION,
        help='Display version information.',
    )

    subparser = parser.add_subparsers(dest='action')

    train.add_arguments(subparser)
    detect.add_arguments(subparser)

    return parser.parse_args(argv)
