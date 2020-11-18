import os
from typing import Generator
from typing import Tuple


def get_path_to(path: str) -> str:
    return os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '../',
            path,
        ),
    )


class NGramIterator:
    def __init__(self, size: int, charset) -> None:
        self.charset = set(charset)
        self.size = size

    def get(self, text: str) -> Generator[Tuple, None, None]:
        filtered = [c for c in text if c in self.charset]
        for start in range(0, len(filtered) - self.size + 1):
            yield tuple(filtered[start:start + self.size])
