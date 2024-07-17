# brealid-python-lib

brealid python library

## Installation

```bash
pip install brealid
```

## Structure

- brealid
  - utils
    - benchmark
  - ctf
    - crypto
      - some useful functions
        - bytes_xor
      - GF2n

## Usage

### ctf

```python
from brealid.ctf import *
from brealid.ctf.crypto import GF2n

print(bytes_xor(b'hello, world', b'\x06\nL\x01\x00^EW\t\x1e\r\x03'))
# b'no more flag'

num = GF2n(0x13) * GF2n(0x13)
print(num)
print(repr(num))
# 261
# GF2n<GaloisField(2^512), poly=0x125> (0x105)
```