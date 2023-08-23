import sqlite3

from typing import NoReturn

from utils import Singleton, py_to_sql_bool


class DomainRepository(metaclass=Singleton):
    # TODO: add ability to mark the domain as unsurfable
    def __init__(self, db_uri: str) -> NoReturn:
        self.db_uri: str = db_uri
        self._create_database_schema()

    def _create_database_schema(self) -> NoReturn:
        with sqlite3.connect(self.db_uri) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS domains( id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, '
                'surfed BOOLEAN NOT NULL DEFAULT FALSE, url STRING NOT NULL UNIQUE);'
            )

    def get_all_not_surfed_domains_ordered_by_id(
        self,
        desc: bool = True
    ) -> list[tuple[int, str]]:
        with sqlite3.connect(self.db_uri) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            return cursor.execute(
                'SELECT id, url FROM domains WHERE surfed = FALSE '
                f'ORDER BY id {"DESC" if desc else "ASC"};'
            ).fetchall()

    def update_domain_surfed_status_by_id(
        self,
        id_: int,
        surfed: bool
    ) -> NoReturn:
        with sqlite3.connect(self.db_uri) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute(f'UPDATE domains SET surfed = {py_to_sql_bool(surfed)} WHERE id = {id_};')

    def create_domain(self, url: str, surfed: bool = False) -> NoReturn:
        with sqlite3.connect(self.db_uri) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute(f'INSERT INTO domains(surfed, url) VALUES({py_to_sql_bool(surfed)}, \'{url}\');')
