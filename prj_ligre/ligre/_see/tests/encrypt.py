#!/bin/env python3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os

def encrypt(key, plaintext):
    iv = os.urandom(16)  # Gera um IV de 16 bytes
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Padding para múltiplo de 16 bytes
    padding_length = 16 - len(plaintext) % 16
    padded_plaintext = plaintext + chr(padding_length) * padding_length

    ciphertext = encryptor.update(padded_plaintext.encode()) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode()

def decrypt(key, b64_ciphertext):
    data = base64.b64decode(b64_ciphertext)
    iv = data[:16]
    ciphertext = data[16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    plaintext_padded = decryptor.update(ciphertext) + decryptor.finalize()
    padding_length = plaintext_padded[-1]
    return plaintext_padded[:-padding_length].decode()

# Exemplo de uso
key = b"12345678901234567890123456789012"  # Chave de 32 bytes
plaintext = "Mensagem secreta"

encrypted = encrypt(key, plaintext)
print("Criptografado:", encrypted)

decrypted = decrypt(key, encrypted)
print("Descriptografado:", decrypted)


quit()

# import hashlib
# import secrets
# import Padding
# import sys
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad
# import base64

# message = 'SSss!#Mais1234'

# plaintext = message
# key = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
# salt = '241fa86763b85341'

# if (len(sys.argv) > 1):
#     plaintext = str(sys.argv[1])
# if (len(sys.argv) > 2):
#     key = str(sys.argv[2])
# if (len(sys.argv) > 3):
#     salt = str(sys.argv[3])


# def get_key_and_iv(password, salt, klen=32, ilen=16, msgdgst='md5'):
#     mdf = getattr(__import__('hashlib', fromlist=[msgdgst]), msgdgst)
#     password = password.encode('ascii', 'ignore')  # convert to ASCII
#     salt = bytearray.fromhex(salt)  # convert to ASCII

#     try:
#         maxlen = klen + ilen
#         keyiv = mdf((password + salt)).digest()
#         tmp = [keyiv]
#         while len(tmp) < maxlen:
#             tmp.append(mdf(tmp[-1] + password + salt).digest())
#             keyiv += tmp[-1]  # append the last byte
#         key = keyiv[:klen]
#         iv = keyiv[klen:klen+ilen]
#         return key, iv
#     except UnicodeDecodeError:
#         return None, None


# def encrypt(plaintext, key, mode, salt):
#     key, iv = get_key_and_iv(key, salt)

#     encobj = AES.new(key, mode, iv)  # type: ignore
#     return (encobj.encrypt(plaintext.encode()))


# def decrypt(ciphertext, key, mode, salt):
#     key, iv = get_key_and_iv(key, salt)
#     encobj = AES.new(key, mode, iv)  # type: ignore
#     return (encobj.decrypt(ciphertext))


# print(f"Plaintext.: {plaintext}")
# print(f"Passphrase: {key}")
# print(f"Salt......: {salt}")
# plaintext = Padding.appendPadding(plaintext, mode='CMS')
# ciphertext = encrypt(plaintext, key, AES.MODE_CBC, salt)
# ctext = b'Salted__' + bytearray.fromhex(salt) + ciphertext

# bd = base64.b64encode(bytearray(ctext)).decode()
# print(f"Cipher (CBC) - Base64: {bd}")
# print(f"Cipher (CBC) - Hex: {ctext.hex()}")
# print(f"Cipher in binary: {ctext}")

# plaintext = decrypt(ciphertext, key, AES.MODE_CBC, salt)
# print(f"Decrypted (Before unpad): {plaintext}")

# plaintext = Padding.removePadding(plaintext.decode(), mode='CMS')
# print(f"Decrypted:{plaintext}")

# quit()

# class Crypt:
#     key = b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
#     iv = b'11111111111aaaaaaaa1111111111111'

#     def __init__(self, key=None, iv=None, cipher=AES.MODE_CBC):
#         self.key = (key or self.key)[:32]
#         self.iv = (iv or self.iv)[:16]
#         self.cipher_mode = cipher

#     def encrypt(self, content):
#         cipher = AES.new(self.key, self.cipher_mode, self.iv)  # type: ignore
#         padded_data = pad(
#             content.encode('utf-8'),
#             AES.block_size,
#             style='pkcs7'
#         )
#         encrypted_data = cipher.encrypt(padded_data)
#         return base64.b64encode(encrypted_data).decode('utf-8')

#     def e(self, input):
#         bs = AES.block_size
#         salt = secrets.token_bytes(bs - len(b'Salted__'))
#         pbk = hashlib.pbkdf2_hmac('sha256', self.key, salt, 10000, 48)
#         key = pbk[:32]
#         iv = pbk[32:48]
#         cipher = AES.new(key, AES.MODE_CBC, self.iv)
#         result = (b'Salted__' + salt)
#         finished = False
#         while not finished:
#             chunk = input.read(1024 * bs).encode()
#             if len(chunk) == 0 or len(chunk) % bs != 0:
#                 padding_length = (bs - len(chunk) % bs) or bs
#                 chunk += (padding_length * chr(padding_length)).encode()
#                 finished = True
#             result += cipher.encrypt(chunk)
#         return result

#     def decrypt(self, encrypted_content):
#         cipher = AES.new(self.key, self.cipher_mode, self.iv)  # type: ignore
#         encrypted_data = base64.b64decode(encrypted_content)
#         decrypted_data = unpad(
#             cipher.decrypt(encrypted_data),
#             AES.block_size,
#             style='pkcs7'
#         )
#         return decrypted_data.decode('utf-8')

#     def d(self, password, salt, key_len, iv_len):
#         """
#         Derive the key and the IV from the given password and salt.
#         """
#         dtot = hashlib.md5(password + salt).digest()
#         d = [dtot]
#         while len(dtot) < (iv_len+key_len):
#             d.append(hashlib.md5(d[-1] + password + salt).digest())
#             dtot += d[-1]
#         return dtot[:key_len], dtot[key_len:key_len+iv_len]


# # Exemplo de uso
# c = Crypt()
# encrypted = c.encrypt(message)
# decrypted = c.decrypt(encrypted)

# print(f"Message.....: {message}")
# print(f"Encrypted...: {encrypted}")
# # print(f"Encrypted2..: {c.e(message)}")
# print(f"Decrypted...: {decrypted}")
