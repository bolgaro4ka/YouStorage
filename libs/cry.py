# crypto.py
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

def encrypt_data(data: bytes, key: bytes) -> bytes:
    """
    Шифрует данные ключом AES-256.
    Возвращает IV (16 байт) + зашифрованные данные.
    """
    if len(key) < 32:
        key = key.ljust(32, b'\0')
    else:
        key = key[:32]

    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(data, AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return iv + encrypted

def decrypt_data(encrypted_data: bytes, key: bytes) -> bytes:
    """
    Дешифрует данные. На входе IV (первые 16 байт) + зашифрованные данные.
    """
    if len(key) < 32:
        key = key.ljust(32, b'\0')
    else:
        key = key[:32]

    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = cipher.decrypt(ciphertext)
    try:
        data = unpad(padded_data, AES.block_size)
    except ValueError:
        raise ValueError("Неверный ключ или поврежденные данные")
    return data