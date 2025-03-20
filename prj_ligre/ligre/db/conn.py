import re
import csv
import mysql.connector
from io import StringIO
from mysql.connector import Error, errorcode, MySQLConnection, CMySQLConnection
from typing import List, Tuple, Dict, Any, Iterator
# from bkpcore.db_config import mysql_conn  # type: ignore
# fmt: off
import Dsn  # type: ignore
# fmt: on


def connect(dsn: str, db: str = None) -> 'Conn_MySQL|None':
    if dsn in Dsn.conf:
        arr = Dsn.conf[dsn]
        if 'type' not in arr:
            return Conn_MySQL(arr, db)
        t = arr['type'].lower()
        if t == 'mysql':
            return Conn_MySQL(arr, db)
        elif t == 'mariadb':
            return Conn_MySQL(arr, db)


class Conn_MySQL:
    def __init__(self, dsn: 'str|Dict', db: str = None) -> None:
        self.verbose = False
        self.db = db
        self.error = None
        self.conn = None

        if not dsn:
            print('Requerido DSN')
            quit()
        conf = self.dsn(dsn) if type(dsn) == str else self.checkConf(dsn)

        if not conf:
            print('DSN inexistente')
            quit()
        if db:
            conf['database'] = db

        self.conn = self.connect(conf)

    def __del__(self):
        self.close()

    def dsn(self, dsn: str) -> dict:
        if dsn not in Dsn.conf:
            return {}
        return self.checkConf(Dsn.conf[dsn])

    def checkConf(self, conf) -> dict:
        default = {
            "host": "localhost",
            "user": None,
            "password": None,
            "database": None,
            "port": 3306,
            "unix_socket": None,
            "auth_plugin": None,
            "charset": "utf8",
            "collation": None,
            "buffered": False,
            "raise_on_warnings": True,
            "use_pure": True,
            "connection_timeout": None,
            "use_unicode": True,
            "ssl_ca": None,
            "ssl_cert": None,
            "ssl_key": None
        }
        out = {}
        for k, v in default.items():
            if k in conf:
                out[k] = conf.get(k, v)
            elif v != None:
                out[k] = v
        return out

    def connect(self, config) -> 'CMySQLConnection|MySQLConnection|None':
        """
        Estabelece e retorna uma conexão com o banco de dados usando a configuração fornecida em mysql_conn.
        """
        try:
            return mysql.connector.connect(**config)  # type: ignore
        except Error as err:
            self.error = err
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print("Erro: ", err)
            return None

    def close(self) -> 'Conn_MySQL':
        if self.conn:
            self.conn.close()
            self.conn = None
        return self

    def query(self, sql: str, param: 'Tuple|List|Dict' = []) -> Iterator[Tuple]:
        """
        Executa uma consulta SQL na base de dados e retorna um iterador sobre os resultados.

        Esta função executa uma consulta SQL fornecida com parâmetros opcionais e retorna um iterador que 
        permite iterar sobre as linhas do resultado da consulta. 

        Parâmetros:
        - sql (str): A string contendo a consulta SQL a ser executada.
        - param (Tuple|List|Dict, opcional): Parâmetros a serem passados para a consulta SQL. Pode ser uma tupla, lista ou dicionário.

        Retorna:
        - Iterator[Tuple]: Um iterador que gera tuplas representando as linhas do resultado da consulta.

        Comportamento:
        1. Se o modo verbose está ativado, imprime o início e o fim da execução da consulta, bem como o SQL formatado.
        2. Cria um cursor para a conexão com a base de dados.
        3. Executa a consulta SQL com os parâmetros fornecidos.
        4. Itera sobre as linhas retornadas pelo cursor e as gera como tuplas.
        5. Fecha o cursor após a iteração sobre todas as linhas.

        Exemplo de uso:
        - Suponha que `sql` seja `'SELECT * FROM users WHERE age > %s'` e `param` seja `(30,)`. 
        A função executará a consulta e retornará um iterador que gera todas as linhas da tabela `users` onde a idade é maior que 30.

        Nota:
        - O cursor é configurado para retornar dicionários (com `dictionary=True`), o que permite acessar os valores das colunas pelo nome.
        - A função usa `yield` para retornar linhas uma por uma, permitindo um processamento eficiente de grandes conjuntos de dados.

        """
        if self.conn:
            self.showSQL(sql, param)
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(sql, param)
            # results = cursor.fetchall()

            for row in cursor:  # type: ignore
                yield row

            cursor.close()

    def fastLine(self, sql: str, param: 'Tuple|List|Dict' = []) -> Dict:
        """
        Executa uma consulta SQL e retorna a primeira linha do resultado como um dicionário.

        Esta função é uma versão simplificada da função `query` que retorna apenas a primeira linha do 
        resultado da consulta, em vez de um iterador. Se a consulta não retornar nenhuma linha, a função 
        retornará um dicionário vazio.

        Parâmetros:
        - sql (str): A string contendo a consulta SQL a ser executada.
        - param (Tuple|List|Dict, opcional): Parâmetros a serem passados para a consulta SQL. Pode ser uma tupla, lista ou dicionário.

        Retorna:
        - Dict: Um dicionário representando a primeira linha do resultado da consulta. Se não houver resultados, retorna um dicionário vazio.

        Comportamento:
        1. Executa a consulta SQL com os parâmetros fornecidos utilizando a função `query`.
        2. Tenta obter a primeira linha do resultado usando `next`.
        3. Se a consulta não retornar nenhuma linha (o que resulta em uma exceção `StopIteration`), retorna um dicionário vazio.

        Exemplo de uso:
        - Suponha que `sql` seja `'SELECT * FROM users WHERE id = %s'` e `param` seja `(1,)`.
        A função executará a consulta e retornará a primeira linha do resultado como um dicionário. Se não houver uma linha com `id = 1`, retornará um dicionário vazio.

        Nota:
        - Utiliza a função `next` para obter a primeira linha do iterador retornado pela função `query`. Isso é eficiente para consultas que se espera que retornem um número limitado de resultados.

        """
        try:
            return next(self.query(sql, param))  # type: ignore
        except StopIteration:
            return {}

    def fastValue(self, sql: str, param: 'Tuple|List|Dict' = []) -> Any:
        """
        Executa uma consulta SQL e retorna o valor da primeira coluna da primeira linha do resultado.

        Esta função é uma versão simplificada da função `query` que retorna apenas o valor da primeira coluna
        da primeira linha do resultado da consulta. Se a consulta não retornar nenhuma linha, a função retornará `None`.

        Parâmetros:
        - sql (str): A string contendo a consulta SQL a ser executada.
        - param (Tuple|List|Dict, opcional): Parâmetros a serem passados para a consulta SQL. Pode ser uma tupla, lista ou dicionário.

        Retorna:
        - Any: O valor da primeira coluna da primeira linha do resultado da consulta. Se não houver resultados, retorna `None`.

        Comportamento:
        1. Executa a consulta SQL com os parâmetros fornecidos utilizando a função `fastLine`.
        2. Se a consulta retornar uma linha, obtém o valor da primeira coluna dessa linha.
        3. Se não houver uma linha, retorna `None`.

        Exemplo de uso:
        - Suponha que `sql` seja `'SELECT name FROM users WHERE id = %s'` e `param` seja `(1,)`.
        A função executará a consulta e retornará o valor da primeira coluna da primeira linha, que neste caso seria o nome do usuário com `id = 1`. Se não houver uma linha com `id = 1`, retornará `None`.

        Nota:
        - Utiliza a função `fastLine` para obter a primeira linha do resultado e, em seguida, usa `next(iter(...))` para obter o valor da primeira coluna dessa linha.
        - É útil quando se espera que a consulta retorne no máximo uma linha e apenas o valor da primeira coluna é relevante.

        """
        first_line = self.fastLine(sql, param)
        if first_line:
            return next(iter(first_line.values()))
        return None

    def queryAll(self, sql: str, param: 'Tuple|List|Dict' = []) -> 'List[Dict]':
        """
        Executa uma consulta SQL e retorna todas as linhas do resultado como uma lista de dicionários.

        Esta função executa uma consulta SQL e coleta todas as linhas retornadas. Cada linha é representada
        como um dicionário onde as chaves são os nomes das colunas e os valores são os valores das colunas
        para aquela linha. A função retorna uma lista contendo todos esses dicionários.

        Parâmetros:
        - sql (str): A string contendo a consulta SQL a ser executada.
        - param (Tuple|List|Dict, opcional): Parâmetros a serem passados para a consulta SQL. Pode ser uma tupla, lista ou dicionário.

        Retorna:
        - List[Dict]: Uma lista de dicionários, onde cada dicionário representa uma linha do resultado da consulta,
        com as chaves sendo os nomes das colunas e os valores sendo os valores das colunas para aquela linha.

        Comportamento:
        1. Executa a consulta SQL com os parâmetros fornecidos utilizando a função `query`.
        2. Itera sobre todas as linhas retornadas pela consulta e adiciona cada linha à lista `row`.
        3. Retorna a lista `row` contendo todas as linhas do resultado.

        Exemplo de uso:
        - Suponha que `sql` seja `'SELECT id, name FROM users'`. A função executará a consulta e retornará uma lista de dicionários,
        onde cada dicionário contém os campos `id` e `name` para cada usuário retornado pela consulta.

        Nota:
        - A função utiliza o método `query`, que é um gerador, para iterar sobre as linhas retornadas pela consulta SQL.
        - A lista retornada pode ser vazia se a consulta não retornar nenhuma linha.

        """
        row = []
        for r in self.query(sql, param):
            row.append(r)
        return row

    def joinParam(self, sql: str, param: 'Tuple|List|Dict' = []) -> str:
        """
        Formata e retorna uma representação da consulta SQL com os parâmetros aplicados.

        Esta função substitui os parâmetros na consulta SQL e retorna a consulta formatada como uma string.
        Se os parâmetros forem fornecidos como um dicionário, eles serão formatados de forma que os valores 
        do tipo string sejam envoltos em aspas duplas, e os valores `None` sejam substituídos por `NULL`.
        Se os parâmetros forem fornecidos como uma tupla ou lista, a mesma formatação será aplicada.

        Parâmetros:
        - sql (str): A string contendo a consulta SQL com placeholders para os parâmetros.
        - param (Tuple|List|Dict, opcional): Parâmetros a serem substituídos na consulta SQL. Pode ser uma tupla, lista ou dicionário.

        Retorna:
        - str: A consulta SQL formatada com os parâmetros aplicados, como uma string.

        Comportamento:
        1. Verifica o tipo de `param`. Se for um dicionário, formata os valores substituindo strings por valores envoltos em aspas duplas,
        e valores `None` por `NULL`. Se for uma tupla ou lista, aplica uma formatação semelhante.
        2. Substitui os placeholders na consulta SQL pelos valores formatados e retorna a consulta reformatada.

        Exemplo de uso:
        - Suponha que `sql` seja `'SELECT * FROM users WHERE name = %s AND age = %s'` e `param` seja `('Alice', 30)`.
        A função retornará a string `'SELECT * FROM users WHERE name = "Alice" AND age = 30'`.

        Nota:
        - A função assume que a consulta SQL utiliza placeholders `%s` para os parâmetros. A substituição é feita diretamente na string SQL.
        - A função `reformat` é utilizada para realizar a formatação final da consulta SQL.

        """
        if type(param) == dict:
            newParam = {k: f'"{v}"' if type(
                v) == str else 'NULL' if v == None else v for k, v in param.items()}
        else:
            newParam = tuple(f'"{v}"' if type(
                v) == str else 'NULL' if v == None else v for v in param)
        # print(sql, newParam)
        return self.reformat(sql % newParam)

    def reformat(self, sql: str) -> str:
        """
        Remove a indentação dos múltiplos níveis de uma consulta SQL e remove linhas em branco.

        Esta função reformata uma consulta SQL, removendo a indentação comum no início de cada linha e 
        eliminando linhas em branco. A indentação é baseada na quantidade de espaços à esquerda na primeira 
        linha não em branco da consulta SQL.

        Parâmetros:
        - sql (str): A string contendo a consulta SQL com múltiplos níveis de indentação e possíveis linhas em branco.

        Retorna:
        - str: A consulta SQL reformulada, com indentação removida e linhas em branco eliminadas.

        Comportamento:
        1. Divide a consulta SQL em linhas com base em quebras de linha.
        2. Remove linhas que estão completamente em branco.
        3. Calcula a quantidade de espaços de indentação na primeira linha não em branco.
        4. Usa uma expressão regular para remover a indentação de todas as linhas.
        5. Junta as linhas reformuladas em uma única string com quebras de linha.

        Exemplo de uso:
        - Suponha que `sql` seja:
        ```
                        SELECT 
                            name,
                            age
                        FROM users
                    WHERE name = 'Alice'
                AND age = 30;
        ```
        A função retornará:
        ```
        SELECT 
            name,
            age
        FROM users
        WHERE name = 'Alice'
        AND age = 30;
        ```

        Nota:
        - A função pressupõe que a indentação é consistente em todas as linhas da consulta SQL.
        - A quantidade de espaços de indentação é calculada com base na primeira linha não em branco.
        """
        lines = sql.splitlines()
        lines = [line for line in lines if line.strip()]
        if not lines:
            return ''
        count_spaces = len(lines[0]) - len(lines[0].lstrip())
        er = re.compile(r'^ {0,'+str(count_spaces)+r'}')
        lines = [er.sub('', line) for line in lines]
        return '\n'.join(lines)

    def exec(self, sql: 'str|List|Tuple', param: 'Tuple|List|Dict' = []) -> 'bool|List':
        """
        Executa uma consulta SQL no banco de dados.

        Este método permite executar uma ou mais consultas SQL. Se a consulta for uma string, ela será executada diretamente. Se a consulta for uma lista ou tupla de strings, cada consulta será executada individualmente. Em caso de erro durante a execução, uma mensagem de erro será exibida.

        Args:
            sql (str|List|Tuple): Consulta SQL a ser executada. Pode ser uma string única ou uma lista/tupla de strings contendo múltiplas consultas.
            param (Tuple|List|Dict, opcional): Parâmetros para a consulta SQL. Se `sql` for uma string, `param` deve ser os parâmetros para essa consulta. Se `sql` for uma lista/tupla, `param` será aplicado a todas as consultas.

        Returns:
            bool|List: Retorna `True` se a consulta foi executada com sucesso, `False` em caso de erro (para consultas individuais). Se `sql` for uma lista/tupla, retorna uma lista de resultados, onde cada item é um booleano indicando o sucesso da execução de cada consulta.

        Example:
            # Executa uma única consulta com sucesso
            success = self.queryExec("INSERT INTO tabela (coluna) VALUES (%s)", ('valor',))

            # Executa múltiplas consultas com sucesso
            results = self.queryExec(["INSERT INTO tabela (coluna) VALUES (%s)", "UPDATE tabela SET coluna = %s WHERE id = %s"], ('valor', 'novo_valor', 1))

            # Exemplo de erro na execução
            success = self.queryExec("INSERT INTO tabela (coluna) VALUES (%s)", ('valor_errado',))
        """
        isok = False
        if not self.conn:
            return isok
        if type(sql) == str:
            cursor = self.conn.cursor()
            try:
                self.showSQL(sql, param)
                cursor.execute(sql, param)
                self.conn.commit()
                isok = True
            except Error as e:
                self.error = e
                self.show(f"Erro ao executar a inserção: {e}")
            if cursor:
                cursor.close()
        else:
            isok = [self.queryExec(i, param) for i in sql]
        return isok

        # Exemplo de uso
        filename = 'exemplo.rar'
        files = self.list_ziped(filename)
        if files:
            print(f"Arquivos no {filename}:")
            for file in files:
                print(file)

    def execMany(self, tbl: str, data: 'List[Dict]', config: Dict = {}):
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

    def str21dict(self, csv_data: str, config: dict = {}) -> 'List[Dict]':
        '''
            Parameters:

                config (dict)
                    f: Iterable[str],
                    delimiter: str = ",",
                    fieldnames: Sequence[str] | None = None,
                    restkey: str | None = None,
                    restval: str | None = None,
                    dialect: _DialectLike = "excel",
                    quotechar: str | None = '"',
                    escapechar: str | None = None,
                    doublequote: bool = True,
                    skipinitialspace: bool = False,
                    lineterminator: str = "\r\n",
                    quoting: _QuotingType = 0,
                    strict: bool = False
        '''
        csv_file = StringIO(csv_data)
        reader = csv.DictReader(csv_file, **config)

        return [row for row in reader]

    def show(self, content):
        if self.verbose:
            print(content)

    def showSQL(self, sql: str, param: 'Tuple|List|Dict' = []):
        if self.verbose:
            lenTitle = 80
            print('Start Query'.center(lenTitle, '-'))
            print(self.joinParam(sql, param))
            print('End Query'.center(lenTitle, '-'))
            print()
            # self.showSQL('\n   -- parameters')
            # self.showSQL(param)
