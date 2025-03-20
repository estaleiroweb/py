#!/bin/python3

# fmt: off
import sys
sys.path.append('/preventive/bin')
import ligre.core.expect as ex
# fmt: on


def test():
    if False:
        # SR/SBC
        host = '10.46.168.5'
        user = 'ipmp'
        passwd = 'ngnInv%2018'
        cmdsDict = {
            'version': 'show version',
            'image': 'show version image',
            'boot': 'show version boot',
            'exit1': 'exit',
            'exit2': 'exit',
        }
    else:
        # ZBHE04
        host = '10.210.17.51'
        user = 'SNGN001'
        passwd = 'P!ruL1t3'
        cmdsDict = {
            'mml': 'mml',
            # 'ioexp': 'ioexp;',
            # 'exit1': 'exit;',
            # 'exit2': 'exit',
        }
    # ex.SSH.verbose = True
    # ex.SSH.verbose = ex.DEBUG_ALL
    # ex.ret_dict = False
    o = ex.SSH(host, user, passwd)
    # ret = o(cmdsDict)
    # ret = o(list(cmdsDict.values()))

    # o.interactive()
    # print('-'*100)
    # print(o.buffer)
    ret = o(['mml','ioexp;', 'exit;', 'exit',])

    print('### Welcome:', o.welcome, sep='\n')
    o.show(ret)


test()
