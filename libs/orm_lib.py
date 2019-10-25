"""this module includes some functions to talk to the database!"""

import sqlite3

def create_data_base(path):

    """creates a database if it doesn't exists, and returns a connection of the data
    base; if the data base exists, it just returns the connection."""

    connection = sqlite3.connect(f'{path}/webider.db')
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS domains("id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "domain" TEXT NOT NULL UNIQUE);')
    cursor.close()

    return connection


def insert_new_domain(cursor, domain):

    """executes a query using by the given cursor that inserts a domain to the
    domains table."""

    cursor.execute('INSERT INTO domains(domain) VALUES(?)', (domain,))


def get_all_domains(cursor, id_greater_than=0):

    """selects all the domains in the domains table which have an greater id than
    given number; if no number were given, it returns all if the domains."""

    cursor.execute('SELECT * FROM domains WHERE id > ?', (id_greater_than,))

    return cursor.fetchall()
