# This file contains the endpoints for the athletes
#Importing the necessary libraries
from fastapi import APIRouter,Depends, HTTPException
from database import get_db,init_db
from utils import get_current_user
from pydantic import BaseModel
import sqlite3
from enum import Enum


router=APIRouter(prefix="/athletes")

class GENDERENUM(str,Enum):
    """
    Enumération des genres possibles pour un athlète.
    """
    male="male"
    female="female"

#schema for the athlete
class AthleteSchema(BaseModel):
    """
    Schéma de données pour un athlète.
    
    Attributes:
        name (str): Nom de l'athlète
        gender (GENDERENUM): Genre de l'athlète (male/female)
        age (int): Âge de l'athlète
        weight (float): Poids de l'athlète en kg
        height (float): Taille de l'athlète en m
        user_id (int): Identifiant de l'utilisateur associé à l'athlète
    """
    name : str
    gender :GENDERENUM
    age : int
    weight : float
    height : float
    user_id : int


#POST CREATE ATHLETE
@router.post('/create')
def create_athlete(athlete: AthleteSchema, db: sqlite3.Connection = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Crée un nouvel athlète dans la base de données.
    
    Args:
        athlete (AthleteSchema): Données de l'athlète à créer
        db (sqlite3.Connection): Connexion à la base de données
        current_user (dict): Informations sur l'utilisateur authentifié
        
    Returns:
        dict: Message de confirmation avec le nom de l'athlète créé
        
    Raises:
        HTTPException 401: Si l'utilisateur n'a pas les droits nécessaires (rôle coach ou admin)
        HTTPException 400: Si l'utilisateur associé n'existe pas
    """
    cursor=db.cursor()
    role=current_user["role"]
    if role !="coach" and role !="admin":
        raise HTTPException(status_code=401, detail="You are not allowed to perform this action")
    try:
        cursor.execute(
            "INSERT INTO athlete(name,gender,age,weight,height,user_id) VALUES(?,?,?,?,?,?)",
            (athlete.name,athlete.gender,athlete.age,athlete.weight,athlete.height,athlete.user_id))
        db.commit()
        # return {f"athlete no.{athlete_id:cursor.lastrowid} created sucessfully" }
        return {f"athlete name : {athlete.name} created sucessfully" }
    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=400, detail="User does not exist") from e


#Get athlete list 
@router.get('/athletes')
def get_athletes(db: sqlite3.Connection = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Récupère la liste de tous les athlètes.
    
    Args:
        db (sqlite3.Connection): Connexion à la base de données
        current_user (dict): Informations sur l'utilisateur authentifié
        
    Returns:
        list: Liste des athlètes enregistrés dans la base de données
        
    Raises:
        HTTPException 401: Si l'utilisateur n'a pas les droits nécessaires (rôle coach ou admin)
    """
    role=current_user["role"]
    if role !="coach" and role !="admin":
        raise HTTPException(status_code=401, detail="You are not allowed to perform this action")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM athlete")
    return cursor.fetchall()


#UPDATE ATHLETE
@router.put('/update/{athlete_id}')
def update_athlete(athlete_id: int, athlete: AthleteSchema, db: sqlite3.Connection = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Met à jour les informations d'un athlète existant.
    
    Args:
        athlete_id (int): Identifiant de l'athlète à mettre à jour
        athlete (AthleteSchema): Nouvelles données de l'athlète
        db (sqlite3.Connection): Connexion à la base de données
        current_user (dict): Informations sur l'utilisateur authentifié
        
    Returns:
        dict: Message de confirmation avec l'identifiant de l'athlète mis à jour
        
    Raises:
        HTTPException 401: Si l'utilisateur n'a pas les droits nécessaires (rôle coach ou admin)
        HTTPException 404: Si l'athlète n'existe pas
    """
    role=current_user["role"]
    if role !="coach" and role !="admin":
        raise HTTPException(status_code=401, detail="You are not allowed to perform this action")
    cursor = db.cursor()
    cursor.execute("UPDATE athlete SET name=?, gender=?, age=?, weight=?, height=?, user_id=? WHERE athlete_id=?",
                   (athlete.name, athlete.gender, athlete.age, athlete.weight, athlete.height, athlete.user_id, athlete_id))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return {f"Athlete no.{athlete_id} updated successfully"}

#DELETE ATHLETE
@router.delete('/delete/{athlete_id}')
def delete_athlete(athlete_id: int, db: sqlite3.Connection = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Supprime un athlète de la base de données.
    
    Args:
        athlete_id (int): Identifiant de l'athlète à supprimer
        db (sqlite3.Connection): Connexion à la base de données
        current_user (dict): Informations sur l'utilisateur authentifié
        
    Returns:
        dict: Message de confirmation avec l'identifiant de l'athlète supprimé
        
    Raises:
        HTTPException 401: Si l'utilisateur n'a pas les droits nécessaires (rôle coach ou admin)
        HTTPException 404: Si l'athlète n'existe pas
    """
    role=current_user["role"]
    if role !="coach" and role !="admin":
        raise HTTPException(status_code=401, detail="You are not allowed to perform this action")
    cursor = db.cursor()
    cursor.execute("DELETE FROM athlete WHERE athlete_id=?", (athlete_id,))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return {f"Athlete no.{athlete_id} deleted successfully"}
