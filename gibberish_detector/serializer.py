"""
Downstream users should not depend on the precise implementations of these serialization functions.
We only assert that:

>>> payload == deserialize(serialize(payload))
"""
from .types import Model


def serialize(model: Model) -> str:
    # Let's just use the most straight-forward serialization model right now.
    # We can always optimize it later.
    import json
    return json.dumps(model)


def deserialize(payload: str) -> Model:
    import json
    return json.loads(payload)
