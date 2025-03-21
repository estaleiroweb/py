from typing import Any, Iterator
from .main import Main


class Dummy(Main):
    """
    Dummy database connection and query handler class.
    Extends the Main class to provide dummy database-specific functionality.
    """

    def select_db(self, db) -> bool:
        return False

    def connect(self, config: dict) -> 'Any':
        pass

    def exec(self, sql: str | list | tuple, param: tuple | list | dict = ...) -> bool | list:
        return False

    def execMany(self, tbl: str, data: list[dict], config: dict = ...):
        pass

    def query(self, conn: Any, sql: str, params: 'Any' = None) -> 'Iterator[Any]':
        return iter([])

    def _checkConfig(self, cfg: dict) -> dict:
        return {}
