import sqlite3

def init_db():
    conn = sqlite3.connect("workout.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            routine_name TEXT,
            exercise TEXT,
            sets INTEGER,
            reps INTEGER,
            duration INTEGER
        )
    ''')
    conn.commit()
    conn.close()
