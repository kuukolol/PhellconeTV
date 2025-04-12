import sqlite3
from pathlib import Path

DB_PATH = Path("phelcone.db")


def create_connection():
    return sqlite3.connect(DB_PATH)


def create_user(username: str, email: str, password_hash: str):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (username, email, password_hash),
    )
    conn.commit()
    conn.close()


def get_user_by_email(email: str):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username, email, password_hash FROM users WHERE email = ?", (email,)
    )
    row = cur.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "password_hash": row[3],
        }
    return None


def get_user_by_username(username: str):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username, email, password_hash FROM users WHERE username = ?",
        (username,),
    )
    row = cur.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "password_hash": row[3],
        }
    return None


def fetch_gadgets():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, brand, name, price FROM gadgets")
    rows = cur.fetchall()
    conn.close()
    gadgets = [
        {"id": row[0], "brand": row[1], "name": row[2], "price": row[3]} for row in rows
    ]
    return gadgets


def fetch_gadgets_by_brand(brand: str):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, brand, name, price FROM gadgets WHERE brand = ?", (brand,))
    rows = cur.fetchall()
    conn.close()
    gadgets = [
        {"id": row[0], "brand": row[1], "name": row[2], "price": row[3]} for row in rows
    ]
    return gadgets
