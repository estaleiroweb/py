"""
String data types.

See:
    - https://dev.mysql.com/doc/refman/8.0/en/char.html
    - https://mariadb.com/kb/en/string-data-types/
"""
from . import main


class Char(main.Type):
    def __init__(self,
                 len: int = 10,
                 not_null: bool = False,
                 auto_increment: bool = False,
                 default: str = None,
                 on_update: str = None,
                 comment: str = None,
                 collate: str = None,
                 expression: str = None,
                 virtual: bool = False,
                 ) -> None:
        self.len: int = len
        self.not_null: bool = not_null
        self.auto_increment: bool = auto_increment
        self.default: str = default
        self.on_update: str = on_update
        self.comment: str = comment
        self.collate: str = collate
        self.expression: str = expression
        self.virtual: bool = virtual

class VarChar(Char):
    pass

class VarChar2(VarChar):
    pass

class Text(VarChar):
    pass

class TinyText(Text):
    pass

class MediumText(Text):
    pass

class Long(Text):
    pass

class LongText(Long):
    pass

class LongVarChar(Long):
    pass

class Bin(Char):
    pass

class Binary(Bin):
    pass

class CharByte(Bin):
    pass

class VarBin(Bin):
    pass

class VarBinary(VarBin):
    pass

class Blob(Bin):
    pass

class TinyBlob(Blob):
    pass

class MediumBlob(Blob):
    pass

class LongBlob(Blob):
    pass

class Enum(VarChar):
    pass

class Set(Enum):
    pass

class UUID(Char):
    pass

class INET4(Char):
    pass

class INET6(INET4):
    pass

class JSON(Enum):
    pass

class Row(Char):
    pass

