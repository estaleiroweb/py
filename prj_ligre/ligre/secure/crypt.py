import base64
import os
from Crypto.Cipher import AES, Blowfish, CAST, DES
from Crypto.Util.Padding import pad, unpad

class Crypt:
    """
    Classe Crypt
    Fornecer funcionalidades de criptografia utilizando PyCryptodome.
    """
    _ciphers = {
        "AES-128-CBC":[AES,AES.MODE_CBC],
        "AES-128-CBC-HMAC-SHA1":[AES,AES.MODE_CBC],
        "AES-128-CFB":[AES,AES.MODE_CFB],
        "AES-128-CFB1":[AES,AES.MODE_CBC],
        "AES-128-CFB8":[AES,AES.MODE_CBC],
        "AES-128-CTR":[AES,AES.MODE_CTR],
        "AES-128-ECB":[AES,AES.MODE_ECB],
        "AES-128-OFB":[AES,AES.MODE_OFB],
        "AES-192-CBC":[AES,AES.MODE_CBC],
        "AES-192-CFB":[AES,AES.MODE_CFB],
        "AES-192-CFB1":[AES,AES.MODE_CFB],
        "AES-192-CFB8":[AES,AES.MODE_CFB],
        "AES-192-CTR":[AES,AES.MODE_CTR],
        "AES-192-ECB":[AES,AES.MODE_ECB],
        "AES-192-OFB":[AES,AES.MODE_OFB],
        "AES-256-CBC":[AES,AES.MODE_CBC],
        "AES-256-CBC-HMAC-SHA1":[AES,AES.MODE_CBC],
        "AES-256-CFB":[AES,AES.MODE_CFB],
        "AES-256-CFB1":[AES,AES.MODE_CFB],
        "AES-256-CFB8":[AES,AES.MODE_CFB],
        "AES-256-CTR":[AES,AES.MODE_CTR],
        "AES-256-ECB":[AES,AES.MODE_ECB],
        "AES-256-OFB":[AES,AES.MODE_OFB],
        "BF-CBC":[Blowfish,Blowfish.MODE_CBC],
        "BF-CFB":[Blowfish,Blowfish.MODE_CFB],
        "BF-ECB":[Blowfish,Blowfish.MODE_ECB],
        "BF-OFB":[Blowfish,Blowfish.MODE_OFB],
        "CAST5-CBC":[CAST,CAST.MODE_CBC],
        "CAST5-CFB":[CAST,CAST.MODE_CFB],
        "CAST5-ECB":[CAST,CAST.MODE_ECB],
        "CAST5-OFB":[CAST,CAST.MODE_OFB],
        "DES-CBC":[DES,DES.MODE_CBC],
        "DES-CFB":[DES,DES.MODE_CFB],
        "DES-CFB1":[DES,DES.MODE_CFB],
        "DES-CFB8":[DES,DES.MODE_CFB],
        "DES-ECB":[DES,DES.MODE_ECB],
        "DES-EDE":[DES,None],
        "DES-EDE-CBC":[DES,DES.MODE_CBC],
        "DES-EDE-CFB":[DES,DES.MODE_CFB],
        "DES-EDE-OFB":[DES,DES.MODE_OFB],
        "DES-EDE3":[DES,None],
        "DES-EDE3-CBC":[DES,DES.MODE_CBC],
        "DES-EDE3-CFB":[DES,DES.MODE_CFB],
        "DES-EDE3-CFB1":[DES,DES.MODE_CFB],
        "DES-EDE3-CFB8":[DES,DES.MODE_CFB],
        "DES-EDE3-OFB":[DES,DES.MODE_OFB],
        "DES-OFB":[DES,DES.MODE_OFB],
    }
    
    def __init__(self, key=None, iv=None, cipher=None): # cipher=AES.MODE_CBC
        self.key = (key or 'chk eVoice @096296 ale# OTAVerde').encode('utf-8')[0:AES.key_size[-1]]
        self.iv = (iv or '78e6a43d0b78c9ef714ec2fb0bb6503c').encode('utf-8')[0:AES.block_size]

    def __call__(self, passwd, decrypt=False):
        return self.decrypt(passwd) if decrypt else self.encrypt(passwd)

    def encrypt(self, text):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypted = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
        return base64.b64encode(encrypted).decode('utf-8')

    def decrypt(self, crypt_text):
        encrypted_data = base64.b64decode(crypt_text)
        # print('encrypted_data',encrypted_data)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        try:
            decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        except Exception as e:
            return None
        return decrypted.decode('utf-8')

    def build_iv(self):
        return os.urandom(AES.block_size)
