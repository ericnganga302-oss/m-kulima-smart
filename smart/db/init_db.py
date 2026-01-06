import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "livestock.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Animals table
cursor.execute("""
CREATE TABLE IF NOT EXISTS animals (
    animal_id TEXT PRIMARY KEY,
    species TEXT,
    birth_date TEXT
)
""")

# Weight records
cursor.execute("""
CREATE TABLE IF NOT EXISTS weights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    animal_id TEXT,
    date TEXT,
    weight REAL,
    FOREIGN KEY(animal_id) REFERENCES animals(animal_id)
)
""")

# Health sensor data
cursor.execute("""
CREATE TABLE IF NOT EXISTS health (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    animal_id TEXT,
    date TEXT,
    temperature REAL,
    activity REAL,
    heart_rate REAL,
    FOREIGN KEY(animal_id) REFERENCES animals(animal_id)
)
""")

conn.commit()
conn.close()

print("✅ Database initialized")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_weights_animal ON weights(animal_id)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_sensors_animal ON sensors(animal_id)")
