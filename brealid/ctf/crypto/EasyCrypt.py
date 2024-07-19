from Crypto.Util.number import *
from Crypto.Cipher import AES
from hashlib import sha384
import pickle
import base64
import os


class EasyCrypt:
    key: bytes
    
    @staticmethod
    def typingEncode(obj):
        if type(obj) == bytes:
            return b'0b' + obj
        elif type(obj) == str:
            return b'0s' + obj.encode()
        else:
            return b'0p' + pickle.dumps(obj)
    
    @staticmethod
    def typingDecode(message: bytes):
        assert message[0:1] == b'0'
        if message[1:2] == b'b':
            return message[2:]
        elif message[1:2] == b's':
            return message[2:].decode()
        elif message[1:2] == b'p':
            return pickle.loads(message[2:])
        else:
            raise ValueError('message broken')
        
    @staticmethod
    def pad(message: bytes, blocklen: int = 16):
        padlen = blocklen - len(message) % blocklen
        return message + bytes([padlen]) * padlen
        
    @staticmethod
    def unpad(message: bytes):
        padlen = message[-1]
        if message[-padlen:] != bytes([padlen]) * padlen:
            raise ValueError('message broken')
        return message[:-padlen]
    
    def __init__(self, key):
        key = EasyCrypt.typingEncode(key)
        self.key = sha384(key).digest()[8:24]
        
    def encrypt(self, data, encoder=base64.b64encode):
        data = EasyCrypt.typingEncode(data)
        data = EasyCrypt.pad(data)
        iv = os.urandom(16)
        aes = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted = iv + aes.encrypt(data)
        encrypted = encoder(encrypted)
        if type(encrypted) == bytes:
            encrypted = encrypted.decode()
        return encrypted
    
    def decrypt(self, data, decoder=base64.b64decode):
        if type(encrypted) == bytes:
            encrypted = encrypted.decode()
        try:
            data = decoder(data)
        except:
            try:
                data = decoder(data.encode())
            except:
                raise ValueError('message broken')
        iv, data = data[:16], data[16:]
        aes = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = aes.decrypt(data)
        decrypted = EasyCrypt.unpad(decrypted)
        decrypted = EasyCrypt.typingDecode(decrypted)
        return decrypted