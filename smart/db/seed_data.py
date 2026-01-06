import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "livestock.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Add animal
cursor.execute("""
INSERT OR IGNORE INTO animals VALUES (?, ?, ?)
""", ("AEG-001", "Cow", "2023-01-15"))

# Add weights
weights = [
    ("AEG-001", "2024-01-01", 300),
    ("AEG-001", "2024-02-01", 305),
    ("AEG-001", "2024-03-01", 312),
]

cursor.executemany("""
INSERT INTO weights (animal_id, date, weight)
VALUES (?, ?, ?)
""", weights)

# Add health data
health = [
    ("AEG-001", "2024-03-01", 38.5, 0.7, 65),
    ("AEG-001", "2024-03-02", 39.8, 0.2, 90),
]

cursor.executemany("""
INSERT INTO health (animal_id, date, temperature, activity, heart_rate)
VALUES (?, ?, ?, ?, ?)
""", health)

conn.commit()
conn.close()

print("✅ Sample data inserted")
