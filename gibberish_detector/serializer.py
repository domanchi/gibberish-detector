"""
Downstream users should not depend on the precise implementations of these serialization functions.
We only assert that:

>>> payload == deserialize(serialize(payload))
"""
from .exceptions import ParsingError
from .model import Model


def serialize(model: Model) -> str:
    # Let's just use the most straight-forward serialization model right now.
    # We can always optimize it later.
    import json
    return json.dumps(model.json())


def deserialize(payload: str) -> Model:
    """
    :raises: ParsingError
    """
    import json

    try:
        data = json.loads(payload)
    except json.decoder.JSONDecodeError:
        raise ParsingError

    return Model.from_dict(data)
