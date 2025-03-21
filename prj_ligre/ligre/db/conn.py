from ..core import fn


def connect(dsn: 'str|dict', db: str = None):
    arr = fn.dsn(dsn)
    if arr:
        t = arr['scheme'].lower() if 'scheme' in arr else 'mysql'
        if t == 'mysql':
            from .mysql import MySQL
            return MySQL(arr, db)
        elif t == 'mariadb':
            from .mariadb import MariaDB
            return MariaDB(arr, db)
    from .dummy import Dummy
    return Dummy(arr, db)
