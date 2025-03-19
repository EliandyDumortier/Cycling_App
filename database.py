import sqlite3


connexion = sqlite3.connect("cycling.db")

cursor = connexion.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT "athlete",        
    )
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS performance (
        performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        vo2max REAL NOT NULL,
        hr_max REAL NOT NULL,
        cadence_max REAL NOT NULL,
        ppo REAL NOT NULL,
        p1 REAL NOT NULL,
        p2 REAL NOT NULL,
        p3 REAL NOT NULL,
        athlete_id INTEGER NOT NULL
        FOREIGN KEY (athlete_id) REFERENCES athlete(athlete_id)
    )
""")