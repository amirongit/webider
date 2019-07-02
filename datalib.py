from sqlite3 import connect

def generate(name):
    conn = connect('webider.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS domains (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, domain TEXT NOT NULL UNIQUE);''')
    conn.commit()
    c.close()
    return conn

def write(domain, cursor):
    cursor.execute('''INSERT INTO `domains`('domain') VALUES("{}")'''.format(domain))

def read(NumberOfRows, cursor):
    cursor.execute('''SELECT * FROM `domains` WHERE id > (SELECT max(id) FROM `domains`) - {}'''.format(NumberOfRows))
    return cursor.fetchall()

def get_max(cursor, table):
    cursor.execute('''SELECT max(id) FROM `{}`'''.format(table))
    return cursor.fetchone()
