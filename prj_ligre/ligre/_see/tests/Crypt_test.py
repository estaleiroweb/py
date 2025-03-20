# /opt/shared/evoice/py/tests/Crypt_test.py
#!/bin/env python3

import json
import sys
import os
__root__ = os.path.dirname(__file__)
while os.path.basename(__root__) != 'py':
    __root__ = os.path.dirname(__root__)
sys.path.append(__root__)

# fmt: off
from Secure.Crypt import Crypt
# fmt: on


# Abrir o arquivo JSON
with open(__root__+'/../dsn.json', 'r', encoding='utf-8') as file:
    # Lê o conteúdo JSON e converte em um dicionário Python
    dados = json.load(file)

# Exibir os dados


crypt = Crypt()
message = 'SSss!#Mais1234'
encrypted = crypt(message)
decrypted = crypt(encrypted, decrypt=True)

print(f"Message..: {message}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")
print(f"OK.......: {message == decrypted}")
dsn = crypt(dados['evoice']['crypt'], True)
print(f"DSN......: {dsn}")
