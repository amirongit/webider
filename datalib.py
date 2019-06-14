from sqlite3 import connect

def generate_db():
    
    "creates a database to use with 'webider'."
    
    connection = connect('webider.db')
    cursor = connection.cursor()

    return {'cursor': cursor, 'connection': connection}

def generate_table(connection):

    "creates the needed tables in a database to use with 'webider'."

    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXIST "domains" ("id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "domain"	TEXT NOT NULL);''')
    connection.commit()


    return True

