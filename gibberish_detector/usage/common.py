import argparse
import os


def valid_file(filename: str) -> str:
    """
    :raises: argparse.ArgumentTypeError
    """
    if not os.path.isfile(filename):
        raise argparse.ArgumentTypeError(f'Invalid file: {filename}')

    return filename
