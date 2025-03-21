import re
from abc import ABC, abstractmethod
from typing import Any, Iterator
from ..core import fn


class Main(ABC):
    """
    Abstract base class for database connection and query handling.

    This class provides a foundation for implementing database-specific connection 
    and query functionality. It defines common interfaces and utility methods for
    database operations that should be consistent across different database types.
    """

    verbose: bool = False
    """Whether to display verbose output about queries and operations."""

    default = {
    }
    """Default configuration values for database connections"""

    def __init__(self, dsn: 'str|dict', db: str = None) -> None:
        """
        Initialize a database connection instance.

        Args:
            dsn (str|dict): Data Source Name as a connection string or a dictionary 
                           containing connection parameters.
            db (str, optional): Database name to select after connection. Defaults to None.

        Raises:
            Fatal error if connection configuration is invalid or incomplete.
        """
        cfg = fn.dsn(dsn)
        if not cfg:
            self.fatal_error('Dada connection config required')

        self.error = None
        """Stores the last error that occurred during database operations"""
        
        self.__dsn: dict = fn.anonymize(cfg)
        self.__conn = self.connect(self._checkConfig(cfg))

        self.db = db

    def __del__(self):
        """
        Destructor method to ensure the database connection is closed when the object is destroyed.

        This method automatically calls the close() method to properly close any open database connection
        when the object is garbage collected.
        """
        self.close()

    @property
    def dsn(self) -> dict:
        """
        Get the configuration of data source by name or URI.

        Returns:
            dict: A dictionary containing the connection parameters with sensitive information masked.
        """
        return self.__dsn

    @property
    def conn(self):
        """
        Get the raw database connection.

        This property provides access to the underlying database connection object
        created by the connect() method.

        Returns:
            Any: The active database connection or None if no connection is established.
        """
        return self.__conn

    @conn.deleter
    def conn(self):
        self.__conn = None

    @property
    def db(self):
        """
        Get the currently selected database or set one.

        Returns:
            str: The name of the currently selected database or None if no database is selected.
        """
        return self.__db

    @db.setter
    def db(self, db):
        if db and db != self.__db and self.select_db(db):
            self.__db = db

    @abstractmethod
    def _checkConfig(self, cfg: dict) -> dict:
        """
        Validates the connection configuration.

        Args:
            cfg (dict): Connection configuration dictionary

        Raises:
            Fatal error if required configuration is missing
        """
        pass

    @abstractmethod
    def connect(self, config):
        """
        Establishes and returns a connection to the database using the provided configuration.

        Args:
            config (dict): MySQL connection configuration parameters

        Returns:
            Any|None: Any database connection object if successful, None otherwise
        """
        pass

    @abstractmethod
    def select_db(self, db) -> bool:
        """
        Changes the current database for the active connection.

        Args:
            db (str): Name of the database to select

        Returns:
            bool: True if database was successfully selected, False otherwise
        """
        pass

    @abstractmethod
    def exec(self, sql: 'str|list|tuple', param: 'tuple|list|dict' = []) -> 'bool|list':
        """
        Execute one or more SQL statements.

        This abstract method should be implemented by subclasses to execute SQL statements
        with the provided parameters. It supports executing a single SQL statement or
        multiple statements.

        Args:
            sql (str|list|tuple): 
                - SQL statement(s) to execute.
                - Can be a single string or a list/tuple of strings for multiple statements.
            param (tuple|list|dict, optional): 
                - Parameters for the SQL statements.
                - If sql is a string, these parameters apply to that statement.
                - If sql is a list/tuple, these parameters apply to all statements.
                - Defaults to empty list.

        Returns:
            bool|list: 
                - True if successful for a single statement
                - List of results for multiple statements
                - False if connection is not available

        Examples:
            ```python
            # Executa uma única consulta com sucesso
            success = self.queryExec("INSERT INTO tabela (coluna) VALUES (%s)", ('valor',))

            # Executa múltiplas consultas com sucesso
            results = self.queryExec(["INSERT INTO tabela (coluna) VALUES (%s)", "UPDATE tabela SET coluna = %s WHERE id = %s"], ('valor', 'novo_valor', 1))

            # Exemplo de erro na execução
            success = self.queryExec("INSERT INTO tabela (coluna) VALUES (%s)", ('valor_errado',))
            ```
        """
        pass

    @abstractmethod
    def execMany(self, tbl: str, data: 'list[dict]', config: dict = {}):
        """
        Executes a batch operation (like INSERT) on multiple rows of data.

        Args:
            tbl (str): Target table name
            data (list[dict]): List of dictionaries containing the data to insert
            config (dict, optional): Configuration for the batch operation. 
                                     Defaults to {'command': 'INSERT'}.

        Returns:
            bool: True if operation was successful, False otherwise
        """
        pass

    @abstractmethod
    def query(self, sql: str, param: 'tuple|list|dict' = []) -> Iterator[tuple]:
        """
        Execute a SQL query and yield results row by row.

        This abstract method should be implemented by subclasses to execute a SQL query
        and return an iterator over the result rows.

        Args:
            sql (str): SQL query string.
            param (tuple|list|dict, optional): Parameters for the query. Defaults to empty list.

        Yields:
            dict: Each row from the query result as a dictionary.

        Examples:
            ```python
            sql='SELECT * FROM users WHERE age > %s'
            param=(30,)
            for row in self.query(sql, param):
                print(row)
            ```
        Notes:
            - If verbose mode is enabled, the method should print the SQL statement and execution details.
            - The cursor should be configured to return dictionaries with column names as keys.
            - The method should use yield to return rows one by one for efficient processing of large datasets.

        Usage:
            1. If verbose mode is enabled, prints the start and end of the query execution, as well as the formatted SQL.
            2. Creates a cursor for the database connection.
            3. Executes the SQL query with the given parameters.
            4. Iterates over the rows returned by the cursor and outputs them as tuples.
            5. Closes the cursor after iterating over all rows.
        """
        pass

    def fastLine(self, sql: str, param: 'tuple|list|dict' = []) -> dict:
        """
        Execute a SQL query and return the first row of the result.

        This method executes a SQL query and returns only the first row of the result
        as a dictionary. If the query returns no rows, an empty dictionary is returned.

        Args:
            sql (str): SQL query string.
            param (tuple|list|dict, optional): Parameters for the query. Defaults to empty list.

        Returns:
            dict: First row of the query result as a dictionary, or empty dictionary if no results.

        See Also: query
        """
        try:
            return next(self.query(sql, param))  # type: ignore
        except StopIteration:
            return {}

    def fastValue(self, sql: str, param: 'tuple|list|dict' = []) -> Any:
        """
        Execute a SQL query and return the first value from the first row.

        This method executes a SQL query and returns the value from the first column
        of the first row. If the query returns no rows, None is returned.

        Args:
            sql (str): SQL query string.
            param (tuple|list|dict, optional): Parameters for the query. Defaults to empty list.

        Returns:
            Any: The value from the first column of the first row, or None if no results.

        See Also: query
        """
        first_line = self.fastLine(sql, param)
        if first_line:
            return next(iter(first_line.values()))
        return None

    def queryAll(self, sql: str, param: 'tuple|list|dict' = []) -> 'list[dict]':
        """
        Execute a SQL query and return all rows as a list of dictionaries.

        This method executes a SQL query and collects all result rows into a list of dictionaries,
        where each dictionary represents one row with column names as keys.

        Args:
            sql (str): SQL query string.
            param (tuple|list|dict, optional): Parameters for the query. Defaults to empty list.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary represents a row from the query result.

        See Also: query
        """
        row = []
        for r in self.query(sql, param):
            row.append(r)
        return row

    def close(self):
        """
        Close the database connection.

        This method closes the active database connection if one exists, and sets
        the internal connection reference to None.
        """
        conn = self.conn
        if conn:
            conn.close()
            conn = None

    def str21dict(self, csv_data: str, config: dict = {}) -> 'list[dict]':
        """
        Convert a CSV string to a list of dictionaries.

        This method parses a CSV string and returns a list of dictionaries, where each dictionary
        represents a row from the CSV with column names as keys.

        Args:
            csv_data (str): CSV data as a string.
            config (dict, optional): Configuration for the CSV reader. Defaults to {}.  
                Supported parameters include:
                - f (Iterable[str]): 
                - delimiter (str): Column separator (default: ',')
                - fieldnames (Sequence[str]): List of column names
                - restkey (str|None) = None,
                - restval (str|None) = None,
                - dialect (_DialectLike) = "excel",
                - quotechar (str): Character for quoting fields (default: '"')
                - escapechar (str): Character for escaping special characters
                - doublequote (bool): Whether to double quotes to escape them (default: True)
                - skipinitialspace (bool): Whether to skip spaces after the delimiter (default: False)
                - lineterminator (str): Line separator (default: '\\r\\n')
                - quoting (_QuotingType): Quoting style (default: 0)
                - strict (bool): Whether to raise exceptions on bad CSV (default: False)

        Returns:
            list[dict]: List of dictionaries, each representing a row from the CSV data.
        """
        import csv
        from io import StringIO

        csv_file = StringIO(csv_data)
        reader = csv.DictReader(csv_file, **config)

        return [row for row in reader]

    def reformat(self, sql: str) -> str:
        """
        Reformat a SQL query by removing indentation and blank lines.

        This method reformats a SQL query by removing common indentation at the beginning of
        each line and eliminating blank lines. The indentation is determined based on the
        leftmost whitespace in the first non-blank line.

        Args:
            sql (str): SQL query string with multiple levels of indentation and possible blank lines.

        Returns:
            str: Reformatted SQL query with indentation removed and blank lines eliminated.

        Example:
            ```python
            sql='        SELECT 
                            name,
                            age
                        FROM users
                    WHERE name = "Alice"'
            print(obj.reformat(sql))
            # Output:
            #    SELECT 
            #        name,
            #        age
            #    FROM users
            #    WHERE name = "Alice"
            ```

        Notes:
            - The function assumes that indentation is consistent across all lines of the SQL query.
            - The amount of indentation spaces is calculated based on the first non-blank line.

        Behavior:
            1. Splits the SQL query into lines based on line breaks.
            2. Removes lines that are completely blank.
            3. Calculates the amount of indentation spaces in the first non-blank line.
            4. Uses a regular expression to remove indentation from all lines.
            5. Joins the reworded lines into a single string with line breaks.
        """
        lines = sql.splitlines()
        lines = [line for line in lines if line.strip()]
        if not lines:
            return ''
        count_spaces = len(lines[0]) - len(lines[0].lstrip())
        er = re.compile(r'^ {0,'+str(count_spaces)+r'}')
        lines = [er.sub('', line) for line in lines]
        return '\n'.join(lines)

    def joinParam(self, sql: str, param: 'tuple|list|dict' = []) -> str:
        """
        Format and return a SQL query with parameters applied.

        This method substitutes parameters into a SQL query string and returns the formatted query.
        String values are wrapped in double quotes, and None values are replaced with NULL.

        Args:
            sql (str): SQL query string with placeholders for parameters.
            param (tuple|list|dict, optional): Parameters to substitute in the query. Defaults to empty list.

        Returns:
            str: Formatted SQL query with parameters applied.

        Examples:
            ```python
            sql = 'SELECT * FROM users WHERE name = %s AND age = %s'
            param = ('Alice', 30)
            print(obj.joinParam(sql,param))
            # Output:
            # SELECT * FROM users WHERE name = "Alice" AND age = 30
            ```
        Notes:
            - The function assumes that the SQL query uses `%s` placeholders for parameters. The replacement is done directly in the SQL string.
            - The `reformat` function is used to perform the final formatting of the SQL query.

        Behavior:
            1. Checks the type of `param`. 
               - If it is a dictionary, formats the values by replacing strings with values enclosed in double quotes, and `None` values with `NULL`. 
               - If it is a tuple or list, applies similar formatting.
            2. Replaces the placeholders in the SQL query with the formatted values and returns the reformatted query.
        """
        if type(param) == dict:
            newParam = {k: f'"{v}"' if type(
                v) == str else 'NULL' if v == None else v for k, v in param.items()}
        else:
            newParam = tuple(f'"{v}"' if type(
                v) == str else 'NULL' if v == None else v for v in param)
        # print(sql, newParam)
        return self.reformat(sql % newParam)

    def fatal_error(self, text):
        """
        Print an error message and terminate the program.

        This method prints the provided error text and exits the program immediately.
        Used for critical errors that prevent further execution.

        Args:
            text (str): Error message to display before terminating.
        """
        print(text)
        quit()

    def show(self, content):
        """
        Display content if verbose mode is enabled.

        This method prints the provided content only if the verbose flag is set to True.

        Args:
            content: The content to display (can be any type that can be printed).
        """
        if self.verbose:
            print(content)

    def showSQL(self, sql: str, param: 'tuple|list|dict' = []):
        """
        Display formatted SQL query with parameters if verbose mode is enabled.

        This method formats the SQL query with its parameters and displays it with
        decorative headers if the verbose flag is set to True.

        Args:
            sql (str): SQL query string with placeholders for parameters.
            param (tuple|list|dict, optional): Parameters to substitute in the query. Defaults to empty list.
        """
        if self.verbose:
            lenTitle = 80
            print('Start Query'.center(lenTitle, '-'))
            print(self.joinParam(sql, param))
            print('End Query'.center(lenTitle, '-'))
            print()
            # self.showSQL('\n   -- parameters')
            # self.showSQL(param)
