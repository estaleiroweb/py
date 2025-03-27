"""
Geometry data types.

See:
    - https://dev.mysql.com/doc/refman/8.0/en/date-and-time-types.html
    - https://mariadb.com/kb/en/date-and-time-data-types/
"""
from . import main

class Point(main.Type):
    def __init__(self,
                 len: int = 0,
                 not_null: bool = False,
                 default: str = None,
                 on_update: str = None,
                 comment: str = None,
                 expression: str = None,
                 virtual: bool = False,
                 ) -> None:
        self.len: int = len
        self.not_null: bool = not_null
        self.default: str = default
        self.on_update: str = on_update
        self.comment: str = comment
        self.expression: str = expression
        self.virtual: bool = virtual

class LineString(Point):
    pass

class Polygon:
    pass

class MultiPoint:
    pass

class MultiLineString:
    pass

class MultiPolygon:
    pass

class Geometrycollection:
    pass

class Geometry:
    pass

