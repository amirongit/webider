from sqlite3 import Cursor, Row
from typing import Any, Type

from dto import DomainDTO


class Singleton(type):
    _instances: dict[Type, Any] = dict()

    def __call__(cls, *args, **kwargs) -> Type[Any]:
        if cls not in cls._instances.keys():
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def domain_row_factory(cursor: Cursor, row: Row) -> DomainDTO:
    return DomainDTO(**dict(zip(list(map(lambda x: x[0], cursor.description)), row)))
