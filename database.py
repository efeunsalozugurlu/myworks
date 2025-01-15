import sqlite3
from datetime import datetime
import csv

# Veritabanı bağlantısını kurar.
def connect_db():
    return sqlite3.connect('accounting.db')

# Tablo oluşturur ve bunu veritabanını bağlar.
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Kullanıcıları tablo haline getirir.
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )''')
    
    # Ürünleri tablo haline getirir.
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        added_by INTEGER,
        FOREIGN KEY(added_by) REFERENCES users(id)
    )''')
    
    # İşlem kayıtlarını tablo haline getirir.
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    # Yapılan değişiklikleri kaydeder.
    conn.commit()
    # Veritabanı bağlantısını keser.
    conn.close()

# Kullanıcıyı eklemek için kullanılan fonksiyon.
def add_user(username, password, role):
    conn = connect_db()
    cursor = conn.cursor()
    # Kullanıcı adı ve şifresi oluşturan kısımdır.
    cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
    conn.commit()
    conn.close()

# Ürün eklemek için kullanılan fonksiyon.
def add_product(name, price, user_id):
    conn = connect_db()
    cursor = conn.cursor()
    # Kullanıcı ID ile kimin ne isimle ve ne fiyatla koyduğu ürünü temsil eder.
    cursor.execute('INSERT INTO products (name, price, added_by) VALUES (?, ?, ?)', (name, price, user_id))
    conn.commit()
    conn.close()

# Ürün silmek için kullanılan fonksiyon.
def delete_product(product_id):
    conn = connect_db()
    cursor = conn.cursor()
    # Ürün ID aracılığıyla ürünü siler.
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()

# Kullanıcıyı silmek için kullanılan fonksiyon.
def delete_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    # Kullanıcı ID aracılığıyla kullanıcıyı siler.
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

# Kullanıcı işlemlerini kaydeden fonksiyon.
def log_action(user_id, action):
    conn = connect_db()
    cursor = conn.cursor()
    # Kullanıcı ID aracılığıyla kullanıcıyı kayıt eder.
    cursor.execute('INSERT INTO logs (user_id, action) VALUES (?, ?)', (user_id, action))
    conn.commit()
    conn.close()

# Kullanıcıların giriş yaparken bilgilerinin doğruluğunu kontrol eden fonksiyon.
def authenticate_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    # Kullanıcı adı ve şifrenin doğruluğunu kontrol eder.
    cursor.execute('SELECT id, role FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Kullanıcının varığını kontrol eden fonksiyon.
def user_exists(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    # Kullanıcı ID aracılığıyla kullanıcının varlığını kontrol eder.
    cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user is not None
# Aynı kullanıcı adının kullanılıp kullanılmadığını kontrol eder.
def username_exists(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Tüm log kayıtlarını CSV dosyasına yazdıran fonksiyon.
def export_logs_to_csv(csv_filename):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM logs')
    logs = cursor.fetchall()
    conn.close()

    with open(csv_filename, 'w', newline='') as csvfile:
        log_writer = csv.writer(csvfile)
        log_writer.writerow(['ID', 'User ID', 'Action', 'Timestamp'])
        log_writer.writerows(logs)
