#copied from users.py
from fastapi import APIRouter, Depends, HTTPException
from utils import get_current_user
from database import get_db
from pydantic import BaseModel
import sqlite3

router=APIRouter(prefix="/performances")


#Schema for the performance
class Performance(BaseModel):
    vo2max: float
    hr_max: float
    rf_max: float
    cadence_max: float
    ppo: float
    p1: float
    p2: float
    p3: float
    athlete_id: int

#POST create athlete performance
@router.post('/create')
def create_performance(performance: Performance,db:sqlite3.Connection = Depends(get_db), current_user=Depends(get_current_user)):
    cursor = db.cursor()
    role=current_user.role
    if role !="coach":
        raise HTTPException(status_code=401, detail="You are not allowed to perform this action")
    try:
        cursor.execute(
                "INSERT INTO performance(vo2max,hr_max,rf_max,cadence_max,ppo,p1,p2,p3,athlete_id) VALUES(?,?,?,?,?,?,?,?,?)",
                (performance.vo2max,performance.hr_max,performance.rf_max,performance.cadence_max,performance.ppo,performance.p1,performance.p2,performance.p3,performance.athlete_id))
        db.commit()
        return {"performance created successfully"}
    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=400, detail="Athlete does not exist") from e
    

#Post modify athlete performance
@router.put('/update/<int:performance_id>')
def update_performance(performance_id: int, performance: Performance, db: sqlite3.Connection = Depends(get_db), current_user=Depends(get_current_user)):
    cursor = db.cursor()
    role=current_user.role
    if role !="coach":
        raise HTTPException(status_code=401, detail="You are not allowed to perform this action")
    cursor.execute("UPDATE performance SET vo2max=?, hr_max=?, rf_max=?, cadence_max=?, ppo=?, p1=?, p2=?, p3=?, athlete_id=? WHERE performance_id=?",
                   (performance.vo2max, performance.hr_max, performance.rf_max, performance.cadence_max, performance.ppo, performance.p1, performance.p2, performance.p3, performance.athlete_id, performance_id))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Performance not found")
    return {f"Performance no.{performance_id} updated successfully"}

#Post delete athlete performance
@router.delete('/delete/<int:performance_id>')
def delete_performance(performance_id: int, db: sqlite3.Connection = Depends(get_db), current_user=Depends(get_current_user)):
    cursor = db.cursor()
    role=current_user.role
    if role !="coach":
        raise HTTPException(status_code=401, detail="You are not allowed to perform this action")
    cursor.execute("DELETE FROM performance WHERE performance_id=?", (performance_id,))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Performance not found")
    return {f"Performance no.{performance_id} deleted successfully"}

#Get all performances (if coach) or get all performances of a specific athlete (if athlete)
@router.get('/performances')
def get_performances(db: sqlite3.Connection = Depends(get_db), current_user=Depends(get_current_user)):
    cursor = db.cursor()
    role=current_user.role
    if role=="coach":
        cursor.execute("SELECT * FROM performance")
        performances = cursor.fetchall()
        return performances
    else:
        cursor.execute("SELECT * FROM performance WHERE athlete_id=?", (current_user.athlete_id,))
        performances = cursor.fetchall()
        return performances