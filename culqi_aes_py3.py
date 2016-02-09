from Crypto.Cipher import AES
from Crypto.Random import random
import base64

AES_MODE = AES.MODE_CBC
IV_LENGTH = 16
BLOCK_SIZE = 16


def _generate_iv():
    return random.Random.get_random_bytes(IV_LENGTH)


def pkcs7_pad(input_bytes):
    l = len(input_bytes)
    val = BLOCK_SIZE - (l % BLOCK_SIZE)
    result = input_bytes + bytearray([val] * val)
    return result


def pkcs7_unpad(input_bytes):
    val = input_bytes[-1]
    if val > BLOCK_SIZE:
        raise ValueError("input_bytes is not padded or padding is corrupt")
    l = len(input_bytes) - val
    result = input_bytes[:l]
    return result


def encrypt(input_str, key):
    input_bytes = input_str.encode()
    key_bytes = base64.decodebytes(key.encode())
    iv = _generate_iv()
    aes = AES.new(key_bytes, AES_MODE, iv)
    encrypted = aes.encrypt(pkcs7_pad(input_bytes))
    return base64.urlsafe_b64encode(iv + encrypted).decode()


def decrypt(input_str, key):
    key_bytes = base64.decodebytes(key.encode())
    input_bytes = base64.urlsafe_b64decode(input_str)
    iv = input_bytes[:IV_LENGTH]
    encrypted = input_bytes[IV_LENGTH:]
    aes = AES.new(key_bytes, AES_MODE, iv)
    return pkcs7_unpad(aes.decrypt(encrypted)).decode()
