import mariadb
# from mysql.connector import FieldType
import pprint
import passwd

# python /AppData/Code/py/my.py

fieldType = {
    0: 'DECIMAL',  # DECIMAL
    1: 'TINYINT',  # TINY
    2: 'SMALLINT',  # SHORT
    3: 'INT',  # LONG
    4: 'FLOAT',  # FLOAT
    5: 'DOUBLE',  # DOUBLE
    6: 'NULL',  # NULL
    7: 'TIMESTAMP',  # TIMESTAMP
    8: 'BIGINT',  # LONGLONG
    9: 'MEDIUMINT',  # INT24
    10: 'DATE',  # DATE
    11: 'TIME',  # TIME
    12: 'DATETIME',  # DATETIME
    13: 'YEAR',  # YEAR
    14: 'NEWDATE',  # NEWDATE
    15: 'VARCHAR',  # VARCHAR
    16: 'BIT',  # BIT
    246: 'DECIMAL',  # NEWDECIMAL
    247: 'ENUM',  # ENUM/INTERVAL
    248: 'SET',  # SET
    249: 'TINYBLOB',  # TINY_BLOB
    250: 'MEDIUMBLOB',  # MEDIUM_BLOB
    251: 'LONGBLOB',  # LONG_BLOB*
    252: 'BLOB',  # BLOB*
    253: 'VARCHAR',  # VAR_STRING
    254: 'CHAR',  # STRING
    254: 'GEOMETRY',  # GEOMETRY
}
# *IS CURRENTLY MAPPED TO ALL TEXT AND BLOB TYPES (MYSQL 5.0.51A)
def myType(tp):
    nType = tp[1]
    tam = 0
    bits = 0
    flags = tp[7]
    mydict = {
        # 'bin_' + tp[0]: f'{bin(flags)[2:]:0>32}',
        'field': tp[0],
        'fieldAlias': tp[9],
        'isNull': tp[6],
        'len': None,
        'nArr': [tp[2], tp[3], tp[4], tp[5]],
        'nBits': None,
        'nFlags': flags,
        'nType': nType,
        'flags': [],
        'precision': None,
        'table': tp[10],
        'tableAlias': tp[8],
        'type': fieldType[nType] if nType in fieldType else f'UNKNOWN_{nType}',
        # 'type_byFT':FieldType.get_info(nType),
    }
    if (flags >> 0) & 1: mydict['flags'].append('NOT NULL')
    if (flags >> 1) & 1: mydict['flags'].append('AUTO_INCREMENT')
    if (flags >> 2) & 1: mydict['flags'].append('UNIQUE')
    if (flags >> 3) & 1: mydict['flags'].append('INDEX')
    if (flags >> 4) & 1: mydict['flags'].append('TEXT')
    if (flags >> 5) & 1: mydict['flags'].append('UNSIGNED')
    if (flags >> 6) & 1: mydict['flags'].append('ZEROFILL')
    if (flags >> 7) & 1: mydict['flags'].append('BLOB')
    if (flags >> 8) & 1: mydict['flags'].append('ENUM')
    if (flags >> 9) & 1: mydict['flags'].append('Flag9')  # TODO
    if (flags >> 10) & 1: mydict['flags'].append('Flag10')  # TODO
    if (flags >> 11) & 1: mydict['flags'].append('SET')
    if (flags >> 12) & 1: mydict['flags'].append('REQUIRED')  # WITHOUT DEFAULT
    if (flags >> 13) & 1: mydict['flags'].append('Flag13')  # TODO
    if (flags >> 14) & 1: mydict['flags'].append('KEY')
    if (flags >> 15) & 1:
        mydict['flags'].append('NUMBER')
        tam = tp[3]
        bits = tp[2] + 1
        if nType in [3, 8]:  # INT,BIGINT
            bits += 1
        elif nType in [4, 5, 246]:  # FLOAT,DOUBLE,DECIMAL
            mydict['precision'] = tp[5]
    elif nType == 252:  # TEXT|BLOB
        if (flags >> 7) & 1:
            b = 'BLOB'
            len = tp[3]
        else:
            b = 'TEXT'
            len = tp[2]
        if (len == 255):
            mydict['type'] = f'TINY{b}'
            bits = 1
            # tinytext: 'tp2': 255,'tp3': 1020 / tinyblob: 'tp2': 63,'tp3': 255
        elif (len == 65535):
            mydict['type'] = b
            bits = 2
            # text: 'tp2': 65535,'tp3': 262140 / blob: 'tp2': 16383,'tp3': 65535
        elif (len == 16777215):
            mydict['type'] = f'MEDIUM{b}'
            bits = 3
            # mediumtext: 'tp2': 16777215,'tp3': 67108860 / mediumblob: 'tp2': 4194303,'tp3': 16777215
        else:
            mydict['type'] = f'LONG{b}'
            bits = 4  # 3FFFFFFF
            # longtext: 'tp2': 1073741823,'tp3': -1 / longblob: 'tp2': 1073741823,'tp3': -1
    elif nType == 253:  # VAR_STRING
        if (flags >> 7) & 1:
            mydict['type'] = 'VARBINARY'
            tam = tp[3]
            # 'tp2': 12,
        else:
            tam = tp[2]
            # 'tp3': 200,
    elif nType == 254:  # STRING
        if (flags >> 7) & 1:
            mydict['type'] = 'BINARY'
            tam = tp[3]
            # 'tp2': 12,
        elif (flags >> 8) & 1:
            mydict['type'] = 'ENUM'
            # 'tp2': 1,'tp3': 4,
        elif (flags >> 11) & 1:
            mydict['type'] = 'SET'
            # 'tp2': 15,'tp3': 60,
        else:
            mydict['type'] = 'CHAR'
            tam = tp[2]
            # 'tp3': 200,
    elif nType == 255:  # GEOMETRY
        mydict['type'] = 'GEOMETRY'
        '''CREATE TABLE tbl_fields_GEOMETRY (
            point POINT,
            linestring LINESTRING,
            polygon POLYGON,
            geometry GEOMETRY,
            multipoint MULTIPOINT,
            multilinestring MULTILINESTRING,
            multipolygon MULTIPOLYGON,
            geometrycollection GEOMETRYCOLLECTION
        )'''
    elif nType in [7, 10, 11, 12, 14]:  # date|time
        tam = tp[5]

    mydict['len'] = tam if tam else None
    mydict['nBits'] = bits if bits else None

    return mydict


try:
    conn = mariadb.connect(**passwd.dsn['evoice'])
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    # sys.exit(1)
cur = conn.cursor()

cur.execute("SELECT a.* FROM Aluno a")

# ('Matricula', 3, 2, 10, 0, 0, True, 32800, 'a', 'Matricula', 'Aluno')
mydict = {
    idx: myType(cur.description[idx])
    for idx in range(len(cur.description))
}

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(mydict)
