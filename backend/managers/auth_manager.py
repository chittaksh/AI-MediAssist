import sqlite3
from sqlite3 import Error

from backend.logger import logging
from pathlib import Path

import os

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR/ "data"  ## Path to the raw data directory
DB_PATH = DATA_DIR / "users.db"

# 3. Create the folder if it doesn't exist
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def create_connection():
    """
    Create a database connection to the SQLite database.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
    except Error as e:
        logging.error(e)
    return conn

def create_table():
    """
    Create the users table in the SQLite database.
    """
    # 1. Initialize Connection & Cursor
    conn = create_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()

        # 2. Create a Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );
        """)

        firstname = os.getenv("FIRSTNAME", "John")
        lastname = os.getenv("LASTNAME", "Doe")
        username = os.getenv("USERNAME", "johndoe")
        password = os.getenv("PASSWORD", "johndoe")

        cursor.execute("""
            INSERT INTO users (firstname, lastname, username, password)
                        VALUES (?, ?, ?, ?)
                    """, (firstname, lastname, username, password))
        conn.commit()

    except Error as e:
        logging.error(f"An error occurred during DB operation: {e}")
        
    finally:
        # 6. Always clean up resources safely
        if conn:
            conn.close()
            logging.info("\nDatabase connection safely closed.")

def create_user(firstname, lastname, username, password) -> bool:
    """
    Create a new user in the SQLite database.
    """
    conn = create_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (firstname, lastname, username, password)
            VALUES (?, ?, ?, ?)
        """, (firstname, lastname, username, password))
        conn.commit()
        return True
    except Error as e:
        logging.error(f"An error occurred while creating user: {e}")
        return False
    finally:
        if conn:
            conn.close()
            logging.info("\nDatabase connection safely closed.")

def login_user(username, password) -> bool:
    """
    Log in a user by checking their credentials.
    """
    conn = create_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM users WHERE username = ? AND password = ?
        """, (username, password))
        user = cursor.fetchone()
        return user is not None
    except Error as e:
        logging.error(f"An error occurred while logging in: {e}")
        return False
    finally:
        if conn:
            conn.close()
            logging.info("\nDatabase connection safely closed.")