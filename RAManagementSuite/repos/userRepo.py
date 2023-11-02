from werkzeug.security import check_password_hash, generate_password_hash
from RAManagementSuite.repos.baseRepo import get_db_connection


def get_user(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user

def create_user(username, password, role):
    conn = get_db_connection()
    conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                 (username, generate_password_hash(password), role))
    conn.commit()
    conn.close()
