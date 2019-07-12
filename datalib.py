from sqlite3 import connect

def generate():

    """creates a database and it's tables to use; it 
    won't delete your database if you already have one;
    also it returns a connection!"""

    conn = connect('webider.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS domains (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, domain TEXT NOT NULL UNIQUE);''')
    conn.commit()
    c.close()

    return conn

def write(domain, cursor):

    """inserts to the table; don't forget to commit
    after calling this fnc."""

    cursor.execute('''INSERT INTO `domains`('domain') VALUES("{}")'''.format(domain))

def read(cursor, NumberOfRows=10):

    """returns a number of the selected 
    values from data base!"""

    cursor.execute('''SELECT * FROM `domains` WHERE id > (SELECT max(id) FROM `domains`) - {}'''.format(NumberOfRows))

    return cursor.fetchall()

def get_max(cursor, table):

    "returns the number of the records in  databse!"

    cursor.execute('''SELECT max(id) FROM `{}`'''.format(table))
    
    return cursor.fetchone()
