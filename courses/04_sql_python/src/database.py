def connect_to_database(db_name):
    import sqlite3
    connection = sqlite3.connect(db_name)
    return connection

def execute_query(connection, query, parameters=()):
    cursor = connection.cursor()
    cursor.execute(query, parameters)
    connection.commit()
    return cursor

def fetch_all_results(cursor):
    return cursor.fetchall()

def close_connection(connection):
    connection.close()