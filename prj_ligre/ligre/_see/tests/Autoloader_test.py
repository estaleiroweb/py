#!/bin/env python3
# /opt/shared/evoice/py/tests/Autoloader_test.py

import sys
import os

# fmt: off
__root__ = os.path.dirname(__file__)
while os.path.basename(__root__) != 'py':
    __root__ = os.path.dirname(__root__)
sys.path.append(__root__)
from Autoloader import al
# fmt: on

print('__root__....: ', __root__)
print('------------------------------------------')
print('Packege.....: ', al.Secure)
print('Módulo......: ', al.module('Secure.Crypt'))
print('Classe......: ', al('Secure.Crypt'))
print('Objeto......: ', al('Secure.Crypt')())
print('Atributo....: ', al.sys.version)
print('------------------------------------------')
f = al.file('tests/dummy.py')
print('FileModule..: ', f)
print('a...........: ', f.a)
print('b...........: ', f.b)
print('c...........: ', f.c)
