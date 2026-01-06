import sqlite3
from pathlib import Path
import pandas as pd

# -------------------------------------------------
# DATABASE SETUP
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "mkulima.db"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()


# -------------------------------------------------
# TABLE INITIALIZATION
# -------------------------------------------------
def init_db():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS animals (
            animal_id TEXT PRIMARY KEY,
            species TEXT NOT NULL,
            birth_date TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            animal_id TEXT NOT NULL,
            weight REAL NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (animal_id) REFERENCES animals (animal_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            animal_id TEXT NOT NULL,
            temperature REAL NOT NULL,
            activity INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (animal_id) REFERENCES animals (animal_id)
        )
    """)

    conn.commit()


# Initialize immediately
init_db()


# -------------------------------------------------
# ANIMAL OPERATIONS
# -------------------------------------------------
def animal_exists(animal_id):
    cursor.execute(
        "SELECT 1 FROM animals WHERE animal_id = ?",
        (animal_id,)
    )
    return cursor.fetchone() is not None


def add_animal(animal_id, species, birth_date):
    if animal_exists(animal_id):
        return False

    cursor.execute("""
        INSERT INTO animals (animal_id, species, birth_date)
        VALUES (?, ?, ?)
    """, (animal_id, species, birth_date))
    conn.commit()
    return True



# -------------------------------------------------
# WEIGHT DATA
# -------------------------------------------------
def add_weight_record(animal_id, weight, date):
    if not animal_exists(animal_id):
        raise ValueError("Animal does not exist")

    cursor.execute("""
        INSERT INTO weights (animal_id, weight, date)
        VALUES (?, ?, ?)
    """, (animal_id, float(weight), date))
    conn.commit()


def load_weight_history(animal_id):
    cursor.execute("""
        SELECT weight
        FROM weights
        WHERE animal_id = ?
        ORDER BY date ASC
    """, (animal_id,))

    rows = cursor.fetchall()
    return [row[0] for row in rows]


# -------------------------------------------------
# SENSOR DATA
# -------------------------------------------------
def add_sensor_record(animal_id, temperature, activity, timestamp):
    if not animal_exists(animal_id):
        raise ValueError("Animal does not exist")

    cursor.execute("""
        INSERT INTO sensors (animal_id, temperature, activity, timestamp)
        VALUES (?, ?, ?, ?)
    """, (animal_id, float(temperature), int(activity), timestamp))
    conn.commit()


def load_sensor_history(animal_id, limit=50):
    cursor.execute("""
        SELECT temperature, activity
        FROM sensors
        WHERE animal_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (animal_id, limit))

    return cursor.fetchall()


# -------------------------------------------------
# BULK CSV HELPERS (OPTIONAL BUT SAFE)
# -------------------------------------------------
def ingest_weights_dataframe(df):
    required = {"animal_id", "weight", "date"}
    if not required.issubset(df.columns):
        raise ValueError("Missing required columns")

    for _, row in df.iterrows():
        if animal_exists(row["animal_id"]):
            add_weight_record(
                row["animal_id"],
                row["weight"],
                row["date"]
            )


def ingest_sensors_dataframe(df):
    required = {"animal_id", "temperature", "activity", "timestamp"}
    if not required.issubset(df.columns):
        raise ValueError("Missing required columns")

    for _, row in df.iterrows():
        if animal_exists(row["animal_id"]):
            add_sensor_record(
                row["animal_id"],
                row["temperature"],
                row["activity"],
                row["timestamp"]
            )
