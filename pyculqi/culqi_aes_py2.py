# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from Crypto.Random import random
import base64

AES_MODE = AES.MODE_CBC
IV_LENGTH = 16
BLOCK_SIZE = 16


def _generate_iv():
    return random.Random.get_random_bytes(IV_LENGTH)


def pkcs7_pad(input_str):
    l = len(input_str)
    val = BLOCK_SIZE - (l % BLOCK_SIZE)
    result = input_str + str(bytearray([val] * val))
    return result


def pkcs7_unpad(input_str):
    val = ord(input_str[-1])
    if val > BLOCK_SIZE:
        raise ValueError("input_str is not padded or padding is corrupt")
    l = len(input_str) - val
    result = input_str[:l]
    return result


def encrypt(input_str, key):
    key_bytes = base64.decodestring(key)
    iv = _generate_iv()
    aes = AES.new(key_bytes, AES_MODE, iv)
    encrypted = aes.encrypt(pkcs7_pad(input_str))
    return base64.urlsafe_b64encode(iv + encrypted)


def decrypt(input_str, key):
    input_str = str(input_str)
    key_bytes = base64.decodestring(key)
    input_bytes = base64.urlsafe_b64decode(input_str)
    iv = input_bytes[:IV_LENGTH]
    encrypted = input_bytes[IV_LENGTH:]
    aes = AES.new(key_bytes, AES_MODE, iv)
    return pkcs7_unpad(aes.decrypt(encrypted))
