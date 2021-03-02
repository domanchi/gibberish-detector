"""
The purpose of the serializer is to compress the `model.json()` for saving to disk.
Downstream users should not depend on the precise implementations of these serialization functions.
We only assert that:

>>> model == deserialize(serialize(model))
"""
import json

from .exceptions import ParsingError
from .model import Model


def serialize(model: Model) -> str:
    data = model.json()
    return json.dumps(data)


def deserialize(payload: str) -> Model:
    """
    :raises: ParsingError
    """
    try:
        raw_data = json.loads(payload)
    except json.decoder.JSONDecodeError:
        raise ParsingError

    return Model.from_dict(raw_data)
