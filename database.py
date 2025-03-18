#Import des libraries
import sqlite3

conn=sqlite3.connect('cycling.db')
cursor=conn.cursor()

#Athlete table

cursor.execute('''CREATE TABLE  [IF NOT EXIST] athlete(
    athlete_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    gender BOOLEAN NOT NULL,
    age INTEGER NOT NULL,
    weight REAL NOT NULL,
    height REAL NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
               )'''
)