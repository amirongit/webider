from sqlite3 import connect

"""all of the methods in this moudle are provided to be used with 'webider'!"""

def generate(name):
    
    "generates a database and it's tables to use on webider!."
    
    ### so we need a connection and a cursor to connect ti the databse and do some queries on it!
    conn = connect('webider.db')
    c = conn.cursor()

    ### and the tables we need!
    c.execute('''CREATE TABLE IF NOT EXISTS domains (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, domain TEXT NOT NULL);''')
    conn.commit()

    return {'cursor': c, 'connection': conn}

def write(domain, connection):
    
    """inserts a domain to the table"""
    
    ### I don't wanna use the main cursor in the program! so just make a cursor to do with this fucntion. 
    ### (increases memory and cpu usage a lot; but it's my choice!)
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO domains(domain) VALUES("{}")'''.format(domain))
    cursor.close()

def read(NumberOfRows, cursor):
    
    """returns last X records on the domains table."""
    
    cursor.execute('''SELECT * FROM domains WHERE id > (SELECT max(id) FROM domains) - {}'''.format(NumberOfRows))
    return cursor.fetchall()

