def get_all_users(conn):
    query = "SELECT * FROM users;"
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def get_user_by_id(conn, user_id):
    query = "SELECT * FROM users WHERE id = ?;"
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    return cursor.fetchone()

def insert_user(conn, user_data):
    query = "INSERT INTO users (name, email) VALUES (?, ?);"
    cursor = conn.cursor()
    cursor.execute(query, user_data)
    conn.commit()
    return cursor.lastrowid

def update_user(conn, user_id, user_data):
    query = "UPDATE users SET name = ?, email = ? WHERE id = ?;"
    cursor = conn.cursor()
    cursor.execute(query, (*user_data, user_id))
    conn.commit()
    return cursor.rowcount

def delete_user(conn, user_id):
    query = "DELETE FROM users WHERE id = ?;"
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    conn.commit()
    return cursor.rowcount