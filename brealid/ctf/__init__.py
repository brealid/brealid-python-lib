from . import crypto
from Crypto.Util.number import bytes_to_long, long_to_bytes

# Alias
def bytes_xor(a: bytes, b: bytes) -> bytes:
    assert len(a) > 0 and len(b) > 0
    if len(a) == 1:
        a = a * len(b)
    elif len(b) == 1:
        b = b * len(a)
    assert len(a) == len(b)
    return long_to_bytes(bytes_to_long(a) ^ bytes_to_long(b), len(a))