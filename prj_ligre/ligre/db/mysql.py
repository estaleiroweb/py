import mysql.connector
from typing import Any, Iterator
from mysql.connector import Error, errorcode, MySQLConnection
from .main import Main


class MySQL(Main):
    """
    MySQL database connection and query handler class.
    Extends the Main class to provide MySQL-specific functionality.
    """
    default = {
        'host': 'localhost',
        'user': None,
        'password': None,
        'database': None,
        'port': 3306,
        'unix_socket': None,
        'auth_plugin': None,
        'charset': "utf8",
        'collation': None,
        'buffered': False,
        'raise_on_warnings': True,
        'use_pure': True,
        'connection_timeout': None,
        'use_unicode': True,
        'ssl_ca': None,
        'ssl_cert': None,
        'ssl_key': None,
    }

    def _checkConfig(self, cfg: dict) -> dict:
        if 'host' not in cfg:
            self.fatal_error('Host connection config required')

        arr = {k: v for k, v in self.default.items() if v is not None}
        for i in cfg:
            if i in self.default and cfg[i] is not None:
                arr[i] = cfg[i]
        return arr

    def connect(self, config: dict) -> 'MySQLConnection|None':
        """
        Establishes and returns a connection to the database using the provided configuration.

        Args:
            config (dict): MySQL connection configuration parameters

        Returns:
            MySQLConnection|None: A MySQL connection object if successful, None otherwise

        Note:
            May return different connection types (MySQLFabricConnection, CMySQLConnection, MySQLConnection)
            depending on the connector implementation.
        """
        try:
            return mysql.connector.connect(**config)   # type: ignore
        except Error as e:
            print(config)
            self.error = e
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.show("Something is wrong with your user name or password")
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                self.show("Database does not exist")
            else:
                self.show(f"Erro: {e}")

    def select_db(self, db: str) -> bool:
        out = False
        conn: 'MySQLConnection|None' = self.conn
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(f"USE {db}")
                conn.database = db
                out = True
            except mysql.connector.Error as e:
                self.error = e
                self.show(f"Erro ao executar a inserção: {e}")
            finally:
                cursor.close()
        return out

    def query(self, sql: str, param: 'tuple|list|dict' = []) -> Iterator[tuple]:
        conn: 'MySQLConnection|None' = self.conn
        if conn:
            self.showSQL(sql, param)
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, param)
            # results = cursor.fetchall()

            for row in cursor:  # type: ignore
                yield row

            cursor.close()

    def exec(self, sql: 'str|list|tuple', param: 'tuple|list|dict' = []) -> 'bool|list':
        isok = False
        conn: 'MySQLConnection|None' = self.conn
        if not conn:
            return isok
        if type(sql) == str:
            cursor = conn.cursor()
            try:
                self.showSQL(sql, param)
                cursor.execute(sql, param)
                conn.commit()
                isok = True
            except Error as e:
                self.error = e
                self.show(f"Erro ao executar a inserção: {e}")
            if cursor:
                cursor.close()
        else:
            isok = [self.queryExec(i, param) for i in sql]
        return isok

    def execMany(self, tbl: str, data: 'list[dict]', config: dict = {}):
        if not data or not self.conn:
            return
        self.show({'tbl': tbl, 'data': data, 'config': config})
        isok = False
        default = {
            'command': 'INSERT',
        }
        config = {**default, **config}
        # print(data[0])
        keys = [k.replace(' ', '_') if k else '' for k in data[0].keys()]
        columns = '`, `'.join(keys)
        # print(keys)
        # print(columns)
        placeholders = ', '.join(['%s'] * len(data[0]))
        sql = \
            config['command']+' ' +\
            tbl+' (`'+columns+'`) ' +\
            'VALUES ('+placeholders+')'
        # print(sql)

        # Extraindo os valores dos dicionários
        values = [tuple(d.values()) for d in data]
        cursor = self.conn.cursor()
        try:
            cursor.executemany(sql, values)
            self.conn.commit()
            isok = True
        except Error as e:
            self.error = e
            self.show(f"Erro ao executar a inserção: {e}")
        if cursor:
            cursor.close()
        return isok
