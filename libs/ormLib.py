import sqlite3

def create_data_base(path):

    connection = sqlite3.connect(f'{path}/webider.db')
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS domains("id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "domain" TEXT NOT NULL UNIQUE);')
    cursor.close()

    return connection


def insert_new_domain(cursor, domain):

    cursor.execute('INSERT INTO domains VALUES(?)', domain)


def get_all_domains(cursor):

    cursor.execute('SELECT domain FROM domains')

    return cursor.fetchall()

