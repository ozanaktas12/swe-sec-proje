import sqlite3
import os
from config import DATABASE_PATH


def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT,
            stock INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS security_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            event_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            source_ip TEXT,
            username TEXT,
            description TEXT,
            payload TEXT,
            blocked INTEGER DEFAULT 0
        );
    """)

    cursor = db.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        _seed_products(db)

    db.commit()
    db.close()


def _seed_products(db):
    products = [
        ("Laptop Pro 15", "High-performance laptop with 16GB RAM", 1299.99, "Electronics", 50),
        ("Wireless Mouse", "Ergonomic wireless mouse with USB receiver", 29.99, "Electronics", 200),
        ("Mechanical Keyboard", "RGB mechanical keyboard, Cherry MX Blue", 89.99, "Electronics", 150),
        ("USB-C Hub", "7-in-1 USB-C hub with HDMI and ethernet", 49.99, "Electronics", 100),
        ("Monitor 27\"", "4K IPS monitor, 60Hz refresh rate", 399.99, "Electronics", 75),
        ("Webcam HD", "1080p webcam with built-in microphone", 59.99, "Electronics", 120),
        ("Headphones", "Noise-cancelling over-ear headphones", 199.99, "Audio", 90),
        ("Bluetooth Speaker", "Portable waterproof bluetooth speaker", 39.99, "Audio", 180),
        ("Phone Case", "Shock-resistant phone case, universal fit", 14.99, "Accessories", 500),
        ("Laptop Stand", "Adjustable aluminum laptop stand", 34.99, "Accessories", 160),
        ("External SSD 1TB", "Portable SSD with USB 3.2", 109.99, "Storage", 80),
        ("Flash Drive 64GB", "USB 3.0 flash drive", 12.99, "Storage", 300),
        ("Network Cable Cat6", "10m ethernet cable", 9.99, "Networking", 400),
        ("Wi-Fi Router", "Dual-band Wi-Fi 6 router", 129.99, "Networking", 60),
        ("Desk Lamp LED", "Adjustable LED desk lamp with USB port", 24.99, "Office", 220),
    ]
    db.executemany(
        "INSERT INTO products (name, description, price, category, stock) VALUES (?, ?, ?, ?, ?)",
        products,
    )


def log_security_event(event_type, severity, description, source_ip=None, username=None, payload=None, blocked=False):
    db = get_db()
    db.execute(
        """INSERT INTO security_logs (event_type, severity, source_ip, username, description, payload, blocked)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (event_type, severity, source_ip, username, description, payload, 1 if blocked else 0),
    )
    db.commit()
    db.close()
