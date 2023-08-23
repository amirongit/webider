from typing import Any, Type


class Singleton(type):
    _instances: dict[Type, Any] = dict()

    def __call__(cls, *args, **kwargs) -> Type[Any]:
        if cls not in cls._instances.keys():
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def py_to_sql_bool(boolean: bool) -> str: return 'TRUE' if boolean else 'FALSE'
