import sqlite3
import os

# Veritabanı dosya adı; testler de bu sabiti kullanacak
DB_NAME = "users.db"

def create_db():
    """
    users tablosunu oluşturur (eğer yoksa).
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            email    TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_user(username, email, password):
    """
    Yeni kullanıcı ekler. Başarılıysa True,
    duplicate veya hata varsa False döner.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    """
    Kullanıcının şifresini doğrular.
    Doğruysa True, değilse False döner.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()
    conn.close()
    return bool(row and row[0] == password)

def display_users():
    """
    Kayıtlı tüm kullanıcıları [(username, email), ...] formatında döner.
    """
    # Veritabanı yoksa önce oluştur
    if not os.path.exists(DB_NAME):
        create_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT username, email FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

