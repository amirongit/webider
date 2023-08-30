import logging
import sqlite3

from threading import current_thread
from typing import NoReturn

import utils

from dto import DomainDTO, DomainQueryDTO


class DomainRepository(metaclass=utils.Singleton):
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

    def get(self, domain_query: DomainQueryDTO) -> list[DomainDTO]:
        with sqlite3.connect(self.db_uri) as conn:
            conn.set_trace_callback(print)
            conn.row_factory = utils.domain_row_factory
            cursor: sqlite3.Cursor = conn.cursor()
            return cursor.execute(self._compile_query(domain_query)).fetchall()

    def create_or_update(self, domain: DomainDTO) -> NoReturn:
        self.create(domain) if domain.id is None else self.update(domain)

    def update(self, domain: DomainDTO) -> NoReturn:
        with sqlite3.connect(self.db_uri) as conn:
            conn.set_trace_callback(print)
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute(
                f'UPDATE domains SET surfed = {str(domain.surfed)}, '
                f'url = \'{domain.url}\' WHERE id = {domain.id};'
            )

    def create(self, domain: DomainDTO) -> NoReturn:
        with sqlite3.connect(self.db_uri) as conn:
            conn.set_trace_callback(print)
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute(
                f'INSERT INTO domains(surfed, url) VALUES({str(domain.surfed)}, \'{domain.url}\');'
            )

    @staticmethod
    def _compile_query(domain_query: DomainQueryDTO):
        query = 'SELECT * FROM domains '

        if len(constraints := list(filter(lambda x: x[1] is not None, domain_query.__dict__.items()))) > 0:
            query_conditions = list()

            for condition, value in constraints:
                if condition == 'id':
                    query_conditions.append(f'id = {str(value)}')
                elif condition == 'url':
                    query_conditions.append(f'url LIKE \'%{value}%\'')
                elif condition == 'surfed':
                    query_conditions.append(f'surfed = {str(value)}')

            query += 'WHERE ' + ' AND '.join(query_conditions)

        return query + ';'
