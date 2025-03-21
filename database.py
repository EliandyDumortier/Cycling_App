import sqlite3
from contextlib import contextmanager

connexion = sqlite3.connect("cycling.db")


def get_db():
    connexion = sqlite3.connect("cycling.db")
    connexion.row_factory = sqlite3.Row
    try:
        yield connexion
    finally:
        connexion.close()


def init_db():
    connexion = sqlite3.connect("cycling.db")

    cursor = connexion.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT "athlete"        
        )
    """)

#Athlete table

    cursor.execute('''CREATE TABLE  IF NOT EXISTS athlete(
        athlete_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        gender TEXT NOT NULL,
        age INTEGER NOT NULL,
        weight REAL NOT NULL,
        height REAL NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES user(user_id)
               )'''
        )

    cursor.execute("""CREATE TABLE IF NOT EXISTS performance (
        performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        vo2max REAL NOT NULL,
        hr_max REAL NOT NULL,
        cadence_max REAL NOT NULL,
        ppo REAL NOT NULL,
        p1 REAL NOT NULL,
        p2 REAL NOT NULL,
        p3 REAL NOT NULL,
        athlete_id INTEGER NOT NULL,
        FOREIGN KEY (athlete_id) REFERENCES athlete(athlete_id)
    )""")
    connexion.commit()
    connexion.close()
                   


@contextmanager
def db_connection():
    conn = sqlite3.connect("cycling.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row 
    try:
        yield conn
    finally:
        conn.close()

def get_db():
    with db_connection() as conn:
        yield conn

if __name__ == "__main" : 
  #initializing the database
  init_db()

