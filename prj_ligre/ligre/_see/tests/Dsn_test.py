#!/bin/env python3
# /opt/shared/evoice/py/tests/Dsn_test.py

from pprint import pprint
import sys
import os
__root__ = os.path.dirname(__file__)
while os.path.basename(__root__) != 'py':
    __root__ = os.path.dirname(__root__)
sys.path.append(__root__)

# fmt: off
from Secure.Dsn import dsn
# fmt: on

pprint({
    '<none>': dsn(),
    'evoice_db1': dsn('evoice_db1'),
})
