import sqlite3

def drop_tokens_table():
    conn = sqlite3.connect('tokens.db')
    cursor = conn.cursor()

    cursor.execute('''
        DROP TABLE IF EXISTS tokens
    ''')

    conn.commit()
    conn.close()

drop_tokens_table()

def create_db():
    conn = sqlite3.connect('tokens.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            access_token TEXT NOT NULL,
            refresh_token TEXT,
            expiration_time DATETIME
        )
    ''')

    conn.commit()
    conn.close()

create_db()

def store_tokens(user_id, access_token, refresh_token, expiration_time):
    conn = sqlite3.connect('tokens.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO tokens (user_id, access_token, refresh_token, expiration_time)
        VALUES (?, ?, ?, ?)
    ''', (user_id, access_token, refresh_token, expiration_time))
    
    conn.commit()
    conn.close()

def get_tokens(user_id):
    conn = sqlite3.connect('tokens.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT access_token, refresh_token, expiration_time, user_id FROM tokens WHERE user_id = ?
    ''', (user_id,))
    
    tokens = cursor.fetchone()
    conn.close()
    
    return tokens

def update_tokens(user_id, access_token, refresh_token, expiration_time):
    conn = sqlite3.connect('tokens.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE tokens 
        SET access_token = ?, refresh_token = ?, expiration_time = ?
        WHERE user_id = ?
    ''', (access_token, refresh_token, expiration_time, user_id))
    
    conn.commit()
    conn.close()