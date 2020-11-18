import string
import tempfile

from gibberish_detector.trainer import train


def test_basic():
    payload = 'abcaca'

    with tempfile.NamedTemporaryFile() as f:
        f.write(payload.encode())
        f.seek(0)

        model = train(f.name, charset=get_charset_from_payload(payload))

    assert model['a']['b'] < model['b']['a']
    assert model['c']['a'] < model['a']['b']


def get_charset_from_payload(payload: str) -> str:
    charset = set([])
    for letter in payload:
        if letter in string.ascii_letters and letter not in charset:
            charset.add(letter)

    return ''.join(sorted(charset))
