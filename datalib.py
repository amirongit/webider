from sqlite3 import connect

def generate(name):
    
    "generates a database and it's tables to use on webider!."
    
    conn = connect('webider.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS domains (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, domain TEXT NOT NULL);''')
    conn.commit()
    c.close()

    return conn

def write(domain, cursor, table):
    
    "inserts a domain to the table, commit after inserting!"
    
    cursor.execute('''INSERT INTO `{}` VALUES("{}")'''.format(table, domain))

def read(NumberOfRows, cursor, table):
    
    "returns last X records on the domains table."
    
    cursor.execute('''SELECT * FROM `{}` WHERE id > (SELECT max(id) FROM `{}`) - {}'''.format(table, table, NumberOfRows))
    
    return cursor.fetchall()

def get_max(cursor, table):
    
    "returns the maximum number of records in a table!"

    cursor.execute('''SELECT max(id) FROM `{}`'''.format(table))

    return cursor.fetchone()
