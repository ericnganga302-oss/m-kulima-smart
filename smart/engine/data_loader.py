import sqlite3
from pathlib import Path
import pandas as pd
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "app_data.db"

def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS animals (
        animal_id TEXT PRIMARY KEY,
        species TEXT,
        birth_date TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS weights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        animal_id TEXT,
        weight REAL,
        date TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS health (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        animal_id TEXT,
        temperature REAL,
        activity INTEGER,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

# ---------- INGESTION ----------

def add_animal(animal_id, species, birth_date):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT OR IGNORE INTO animals VALUES (?, ?, ?)",
        (animal_id, species, birth_date)
    )
    conn.commit()
    conn.close()

def add_weight(animal_id, weight):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO weights (animal_id, weight, date) VALUES (?, ?, ?)",
        (animal_id, weight, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def add_health(animal_id, temperature, activity):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO health (animal_id, temperature, activity, date) VALUES (?, ?, ?, ?)",
        (animal_id, temperature, activity, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

# ---------- LOADERS ----------

def load_weight_history(animal_id):
    conn = get_conn()
    df = pd.read_sql(
        "SELECT weight, date FROM weights WHERE animal_id=? ORDER BY date",
        conn,
        params=(animal_id,)
    )
    conn.close()
    return df

def load_health_latest(animal_id):
    conn = get_conn()
    df = pd.read_sql(
        """
        SELECT temperature, activity, date
        FROM health
        WHERE animal_id=?
        ORDER BY date DESC LIMIT 1
        """,
        conn,
        params=(animal_id,)
    )
    conn.close()
    return df
