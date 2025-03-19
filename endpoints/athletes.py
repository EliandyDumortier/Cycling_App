# This file contains the endpoints for the athletes
#Importing the necessary libraries
from fastapi import APIRouter,Depends, HTTPException
from database import get_db,init_db
from pydantic import BaseModel
import sqlite3
from enum import Enum



router=APIRouter(prefix="/athletes")

class GENDERENUM(str,Enum):
    male="male"
    female="female"

#schema for the athlete
class AthleteSchema(BaseModel):
    name : str
    gender :GENDERENUM
    age : int
    weight : float
    height : float
    user_id : int


#POST CREATE ATHLETE
@router.post('/create')
def create_athlete(athlete: AthleteSchema,db: sqlite3.Connection = Depends(get_db)):
    cursor=db.cursor()
    try:
        cursor.execute(
            "INSERT INTO athlete(name,gender,age,weight,height,user_id) VALUES(?,?,?,?,?,?)",
            (athlete.name,athlete.gender,athlete.age,athlete.weight,athlete.height,athlete.user_id))
        db.commit()
        # return {f"athlete no.{athlete_id:cursor.lastrowid} created sucessfully" }
        return {f"athlete name : {athlete.name} created sucessfully" }
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="User does not exist")
    


#Get athlete list 
@router.get('/athletes')
def get_athletes(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM athlete")
    athletes = cursor.fetchall()
    return athletes


#UPDATE ATHLETE
@router.put('/update/<int:athlete_id>')
def update_athlete(athlete_id: int, athlete: AthleteSchema, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("UPDATE athlete SET name=?, gender=?, age=?, weight=?, height=?, user_id=? WHERE athlete_id=?",
                   (athlete.name, athlete.gender, athlete.age, athlete.weight, athlete.height, athlete.user_id, athlete_id))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return {f"Athlete no.{athlete_id} updated successfully"}

#DELETE ATHLETE
@router.delete('/delete/<int:athlete_id>')
def delete_athlete(athlete_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM athlete WHERE athlete_id=?", (athlete_id,))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return {f"Athlete no.{athlete_id} deleted successfully"}