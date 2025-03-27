import sys
import os

# py /preventive/bin/py/prj_ligre/ligre/_see/tests/test_extract.py

# fmt: off
import add_path
add_path.up('ligre')
import ligre.core.expect as ex
from ligre.core.conf import Conf
from ligre.db import conn
# fmt: on

# evoice=conn.connect('evoice')
# res=evoice.queryAll('show databases')
# print(res)
# quit()


def test():
    key = 'ZBHE04'
    if key == 'SDVBHE04':
        cmdsDict = {
            'version': 'show version',
            'image': 'show version image',
            'boot': 'show version boot',
            'exit1': 'exit',
            'exit2': 'exit',
        }
        prompt = 'auto'
    elif key == 'ZBHE04':
        cmdsDict = {
            'mml': 'mml',
            'ioexp': 'ioexp;',
            'exit1': 'exit;',
            'exit2': 'exit',
        }
        prompt = 'msc'
    else:
        return

    cfg = Conf('devices.json')
    cfg = cfg()
    if not isinstance(cfg, dict) or key not in cfg:
        return
    cfg = cfg[key]
    # ex.SSH.verbose = True
    # ex.SSH.verbose = ex.DEBUG_ALL
    # ex.ret_dict = False
    o = ex.SSH(cfg['host'], cfg['user'], cfg['passwd'], prompt=prompt)
    # o.prompt = prompt
    ret = o(cmdsDict)
    # ret = o(list(cmdsDict.values()))

    # o.interactive()
    # print('-'*100)
    # print(o.buffer)
    # ret = o(['mml','ioexp;', 'exit;', 'exit',])

    print('### Welcome:', o.welcome, sep='\n')
    print('-'*100)
    o.show(ret)


test()
