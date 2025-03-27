from . import fields, keys, constraints, foreignKey, partitions, sql, data

class Table():
    conn: 'str|None' = None
    """Connection of the database."""

    engine: 'str|None' = None
    """Engine of the table."""

    name: 'str|None' = None
    """Name of the table."""

    label: 'str|None' = None
    """Label of the table. If None, use the name."""

    db: 'str|None' = None
    """Database schema of the table."""

    collate: 'str|None' = None
    """Collate of the table."""

    row_format: 'str|None' = None
    """Row format of the table"""

    checksum: 'bool' = False
    """Indicates whether the table has a checksum. Defaults to False."""

    avg_row_length: 'int|None' = None
    """Average row length of the table."""

    max_rows: 'int|None' = None
    """Maximum number of rows in the table."""

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return ''

    def test(self) -> bool:
        """Test the table"""
        return True

    class fields(fields.Fields):
        pass

    class keys(keys.Keys):
        pass

    class constraints(constraints.Constraints):
        pass

    class foreignKey(foreignKey.ForeignKey):
        pass

    class partitions(partitions.Partitions):
        pass

    class sql(sql.SQL):
        pass

    class data(data.Data):
        pass