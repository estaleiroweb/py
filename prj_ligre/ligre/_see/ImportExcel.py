#!/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import glob
import pandas as pd
import re
import math
import numbers
import csv
import tempfile
from pandas.core.frame import DataFrame as pdDf

# __dir__ = os.path.dirname(os.path.abspath(__file__))

# global parameters
encoding = 'utf8'
engines = {
    'xls': None,  # xlrd
    'xlsm': None,
    'xlsx': 'openpyxl',
    'xlsb': 'pyxlsb',
    'odf': 'odf',  # odfpy
    'ods': 'odf',  # odfpy
    'odt': 'odf',  # odfpy
}


def openXLS(f):
    global file, dir, df, extensao
    file = f
    if not os.path.isfile(file):
        print("File doesn't exist: " + file)
        quit()
    dir = os.path.dirname(file)
    # defined a file in this point
    extensao = re.findall("\.([^.]+)$", file)[0]

    # check if file has a supported extension
    e = engines.keys()
    if extensao not in e:
        print('Not accepted format: ' + extensao)
        print('Accepted formats:' + ', '.join(e))
        quit()

    # load sheets
    print("Opening file: " + file)
    df = pd.read_excel(file, sheet_name=None, engine=engines[extensao])
    print("Ready")


def reDir(rootdir: str, pattern: str, recursive: bool = False) -> list:
    """funtion to get directory by regular expression

    Args:
        rootdir (str): _description_
        pattern (str): _description_
        recursive (bool, optional): _description_. Defaults to False.

    Returns:
        list: _description_
    """
    regex = re.compile(pattern)
    lst = []
    for root, dirs, files in os.walk(rootdir):
        for f in files:
            if regex.search(f):
                if not recursive and rootdir != root: break
                lst.append(root + '/' + f)
    return lst


def myExec(sql) -> None:
    # fileName='/tmp/pythonImportSQL'
    tf = tempfile.NamedTemporaryFile()
    fileName = tf.name
    tf.close()

    with open(fileName, 'w') as fs:
        fs.write(sql)
    # sql = sql.replace('`', '\\`')
    # sql = sql.replace('"', '""')
    # print(sql)
    # ret = os.system(f'mysql -e "{sql}"')
    ret = os.system(f'mysql < "{fileName}"')
    if ret > 0:
        print(f'Query: {sql}')
        quit()


def rebuildDataFrame(df: pdDf, cfg: list) -> pdDf:
    # if cfg[1]:
    #     lst = df.iloc[cfg[1] - 1].values.tolist()
    #     while clearLabel(lst.pop()) == '':
    #         df = df.drop(columns=df.columns[-1])
    if len(cfg) > 3:
        fn = cfg[3]
        if callable(fn): df = fn(df, cfg)
        else: df = globals()[fn](df, cfg)
    # print(df[df.columns[[0, 1, 2, 3, 4, 5]]])
    return df


def importRoboc(df: pdDf,
                cfg: list,
                fullFilename: str,
                loadData_param_set='') -> None:
    # os.system(f'cat "{loc}"')
    # print('----------------------')
    if cfg[2] == None:
        fields = ''
    else:
        cols = [f'@c{item}' for item in range(1, len(df.columns.values) + 1)]
        fields = f'''
            ({','.join(cols)})
            SET {cfg[2]}
        '''
    print('- Load Data')
    myExec(f'TRUNCATE TABLE {cfg[0]}')
    sql = f"""
        LOAD DATA INFILE '{fullFilename}'
        IGNORE INTO TABLE {cfg[0]}
        CHARACTER SET {encoding}
        FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\\\'
        LINES TERMINATED BY '\n'
        IGNORE {cfg[1]+1} LINES {fields}
    """ + loadData_param_set
    # FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\'
    # print(sql)
    # os.system(f'cat "{fullFilename}"')
    myExec(sql)


def clearLabel(val) -> str:
    t = type(val)
    if t == str:
        val = re.sub(r'^Unnamed: \d+$', '', val)
        val = re.sub(r'\.\d+$', '', val)
    elif isinstance(val, numbers.Number) and math.isnan(val):
        val = ''
    else:
        val = str(val)
    return val.replace('-', '_')


def ajustHeader(lst: list) -> list:
    old = ''
    for i in range(0, len(lst)):
        lst[i] = clearLabel(lst[i])
        if lst[i] == '': lst[i] = old
        else: old = lst[i]
    return lst


def getHeader(df: pdDf, nRow: int, inHeader: list = []) -> list:
    header = [clearLabel(item) for item in df.columns.values]
    if nRow > 0:
        rng = range(0, len(header))
        # h = df.iloc[0:nRow].values.tolist()
        for line in df.iloc[0:nRow].values.tolist():
            line = ajustHeader(line)
            for i in rng:
                if line[i] != '':
                    header[
                        i] = f'{line[i]}{"_" if header[i]!="" else ""}{header[i]}'
    for i in range(0, len(inHeader)):
        header[i] = inHeader[i]
    return header


def createTable(cfg, header) -> None:
    print(f'- Create Table {cfg[0]}')
    fields = [f'`{item}` VARCHAR(100)' for item in header]
    fields = ',\n\t'.join(fields)
    myExec(f'CREATE OR REPLACE TABLE {cfg[0]} (\n\t{fields}\n)')


def importFile(imp, procedure=None):
    exportPath = 'csv'
    # check/create destination directory
    fullExportPath = dir + '/' + exportPath
    print('Destination path: ' + fullExportPath)
    if not os.path.isdir(fullExportPath):
        dest = os.mkdir(fullExportPath)
        if dest == '' or dest == None:
            print('Create destination path error: ' + fullExportPath)
            quit()
    filelist = glob.glob(os.path.join(fullExportPath, "*"))
    for f in filelist:
        os.remove(f)

    # quit()
    # load and export sheet
    impKeys = imp.keys()
    for sheet in df.keys():
        if sheet in impKeys:
            print('# Creating CSV from sheet: ' + sheet)
            location = fullExportPath + '/' + sheet + '.csv'
            df[sheet].dropna(how='all')
            df[sheet] = rebuildDataFrame(df[sheet], imp[sheet])
            df[sheet].to_csv(location,
                             encoding=encoding,
                             index=False,
                             sep=',',
                             quoting=csv.QUOTE_ALL,
                             quotechar='"',
                             escapechar="\\",
                             line_terminator='\n')
            importRoboc(df[sheet], imp[sheet], location)
        else:
            print('# Ignore sheet: ' + sheet)

    if procedure is not None:
        print('Call Procedure')
        myExec('CALL ' + procedure)
