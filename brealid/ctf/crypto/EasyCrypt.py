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
    
    def __init__(self, key):
        key = EasyCrypt.typingEncode(key)
        self.key = sha384(key).digest()[8:24]
        
    def encode(self, data):
        data = EasyCrypt.typingEncode(data)
        iv = os.urandom(16)
        aes = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted = iv + aes.encrypt(data)
        encrypted = base64.b64encode(encrypted).decode()
        return encrypted
    
    def decode(self, data):
        if type(data) is str:
            data = data.decode()
        elif type(data) is bytes:
            pass
        else:
            raise ValueError('message broken')
        data = base64.b64decode(data)
        iv, data = data[:16], data[16:]
        aes = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = aes.decrypt(data)
        decrypted = EasyCrypt.typingDecode(decrypted)
        return decrypted