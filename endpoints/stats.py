# Description: This file contains the endpoints for the stats of the athletes
#importing the necessary libraries
from fastapi import APIRouter,Depends, HTTPException
from database import get_db
from utils import get_current_user
import sqlite3

#creating the router
router=APIRouter(prefix="/stats")

#athlete with the highest Vo2max
@router.get('/vo2max')
def vo2max(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT athlete_id, name, MAX(vo2max) FROM performance group by athlete_id,name")
    return cursor.fetchone()

#the most powerful athlete
@router.get('/ppo')
def ppo(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT athlete_id, name, MAX(ppo) FROM performance group by athlete_id,name")
    return cursor.fetchone()

#athlete with the best rapport ppo/weight
@router.get('/weightpower')
def weightpower(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT athlete_id, name, MAX(ppo/weight) FROM performance group by athlete_id,name")
    return cursor.fetchone()

