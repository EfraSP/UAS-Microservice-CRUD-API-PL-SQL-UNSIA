from database import conn
from crypt import encrypt, decrypt

def create_user(username, password):
    cur = conn.cursor()
    encrypted_password = encrypt(key, password.encode())
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, encrypted_password))
    cur.close()

def get_user(username):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    return user

def update_user_password(username, new_password):
    cur = conn.cursor()
    encrypted_password = encrypt(key, new_password.encode())
    cur.execute("UPDATE users SET password = %s WHERE username = %s", (encrypted_password, username))
    cur.close()

def delete_user(username):
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username = %s", (username,))
    cur.close()
