from math import gcd
from Crypto.Util.number import inverse
    
def galois_mul(x, y, bits = 512, poly = 0x125):
    r = 0
    for b in range(bits - 1, -1, -1):
        r <<= 1
        if y & (1 << b):
            r ^= x
        if r & (1 << bits):
            r ^= (1 << bits) | poly
    return r

def galois_pow(x, y, bits = 512, poly = 0x125):
    r = 1
    while y:
        if y & 1:
            r = galois_mul(r, x, bits, poly)
        y >>= 1
        x = galois_mul(x, x, bits, poly)
    return r
    
class GaloisNumber_2n:
    def __init__(self, n = 0, bits = 512, poly = 0x125) -> None:
        self.__n = abs(n)
        self.__bits = bits
        self.__poly = poly
    
    def ringLength(self) -> int:
        return 2**self.__bits - 1
 
    def __repr__(self) -> str:
        return f'GF2n<GaloisField(2^{self.__bits}), poly={hex(self.__poly)}> ({hex(self.__n)})'
    
    def __mul__(self, y) -> None:
        if type(y) is not GaloisNumber_2n:
            y = GaloisNumber_2n(y, self.__bits, self.__poly)
        else:
            assert self.__bits == y.__bits and self.__poly == y.__poly
        return GaloisNumber_2n(galois_mul(self.__n, y.__n, self.__bits, self.__poly), self.__bits, self.__poly)
    
    def __rmul__(self, y) -> None:
        return self * y
    
    def __pow__(self, y) -> None:
        if type(y) == GaloisNumber_2n:
            y = y.__n
        return GaloisNumber_2n(galois_pow(self.__n, y % self.ringLength(), self.__bits, self.__poly), self.__bits, self.__poly)
    
    def __xor__(self, y) -> None:
        if type(y) is not GaloisNumber_2n:
            y = GaloisNumber_2n(y, self.__bits, self.__poly)
        else:
            assert self.__bits == y.__bits and self.__poly == y.__poly
        return GaloisNumber_2n(self.__n ^ y.__n, self.__bits, self.__poly)
    
    def __add__(self, y) -> None:
        return self ^ y
    
    def __radd__(self, y) -> None:
        return self ^ y
    
    def __sub__(self, y) -> None:
        return self ^ y
    
    def __rsub__(self, y) -> None:
        return self ^ y

    def __truediv__(self, y) -> None:
        if type(y) is not GaloisNumber_2n:
            y = GaloisNumber_2n(y, self.__bits, self.__poly)
        else:
            assert self.__bits == y.__bits and self.__poly == y.__poly
        return self * (y ** (2**self.__bits - 2))

    def __rtruediv__(self, y) -> None:
        if type(y) is not GaloisNumber_2n:
            y = GaloisNumber_2n(y, self.__bits, self.__poly)
        else:
            assert self.__bits == y.__bits and self.__poly == y.__poly
        return y * (self ** (2**self.__bits - 2))

    def __eq__(self, y) -> None:
        if type(y) is not GaloisNumber_2n:
            return self.__n == y
        else:
            assert self.__bits == y.__bits and self.__poly == y.__poly
            return self.__n == y.__n

    def __ne__(self, y) -> None:
        if type(y) is not GaloisNumber_2n:
            return self.__n != y
        else:
            assert self.__bits == y.__bits and self.__poly == y.__poly
            return self.__n != y.__n

    def __neg__(self) -> None:
        if self.__n == 0:
            return self
        return GaloisNumber_2n(2**self.__bits - 1 - self.__n, self.__bits, self.__poly)

    def __pos__(self) -> None:
        return self

    def __invert__(self) -> None:
        return self

    def __int__(self) -> None:
        return self.__n

    def __str__(self) -> None:
        return str(self.__n)

    def sqrt(self) -> None:
        return self ** (2**(self.__bits-1))

    def iroot(self, kth) -> None:
        if gcd(kth, self.ringLength()) != 1:
            raise AssertionError('GF2n.iroot: kth and self.ringLength() must be coprime')
        return self ** inverse(kth, self.ringLength())

