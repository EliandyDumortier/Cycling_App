from fastapi import APIRouter, Depends, HTTPException
from utils import get_current_user
from database import get_db
from pydantic import BaseModel
import sqlite3

router=APIRouter(prefix="/performances")

class Performance(BaseModel):
    """Schéma de données pour les performances d'un athlète.

    Attributes:
        vo2max (float): Consommation maximale d'oxygène de l'athlète
        hr_max (float): Fréquence cardiaque maximale
        rf_max (float): Fréquence respiratoire maximale
        cadence_max (float): Cadence maximale
        ppo (float): Puissance maximale (Peak Power Output)
        p1 (float): Puissance zone 1
        p2 (float): Puissance zone 2
        p3 (float): Puissance zone 3
        athlete_id (int): Identifiant unique de l'athlète associé
    """
    vo2max: float
    hr_max: float
    rf_max: float
    cadence_max: float
    ppo: float
    p1: float
    p2: float
    p3: float
    athlete_id: int

@router.post('/create')
def create_performance(performance: Performance, db:sqlite3.Connection = Depends(get_db), current_user=Depends(get_current_user)):
    """Crée une nouvelle performance pour un athlète.

    Args:
        performance (Performance): Les données de performance à enregistrer
        db (sqlite3.Connection): Connexion à la base de données
        current_user (dict): Utilisateur actuellement connecté

    Returns:
        dict: Message de confirmation de création

    Raises:
        HTTPException 401: Si l'utilisateur n'a pas les droits nécessaires (role coach ou admin)
        HTTPException 400: Si l'athlète associé n'existe pas dans la base de données
    """
    cursor = db.cursor()
    role=current_user["role"]
    if role not in ["coach", "admin"]:
        raise HTTPException(status_code=401, detail="You are not allowed to perform this action")
    try:
        cursor.execute(
                "INSERT INTO performance(vo2max,hr_max,hr_max,cadence_max,ppo,p1,p2,p3,athlete_id) VALUES(?,?,?,?,?,?,?,?,?)",
                (performance.vo2max,performance.hr_max,performance.hr_max,performance.cadence_max,performance.ppo,performance.p1,performance.p2,performance.p3,performance.athlete_id))
        db.commit()
        return {"performance created successfully"}
    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=400, detail="Athlete does not exist") from e

@router.put('/update/<int:performance_id>')
def update_performance(performance_id: int, performance: Performance, db: sqlite3.Connection = Depends(get_db), current_user=Depends(get_current_user)):
    """Met à jour les données de performance d'un athlète.

    Args:
        performance_id (int): Identifiant de la performance à modifier
        performance (Performance): Nouvelles données de performance
        db (sqlite3.Connection): Connexion à la base de données
        current_user (dict): Utilisateur actuellement connecté

    Returns:
        dict: Message de confirmation avec l'ID de la performance modifiée

    Raises:
        HTTPException 401: Si l'utilisateur n'a pas les droits nécessaires (role coach ou admin)
        HTTPException 404: Si la performance n'est pas trouvée dans la base de données
    """
    cursor = db.cursor()
    role=current_user["role"]
    if role not in ["coach", "admin"]:
        raise HTTPException(status_code=401, detail="You are not allowed to perform this action")
    cursor.execute("UPDATE performance SET vo2max=?, hr_max=?, rf_max=?, cadence_max=?, ppo=?, p1=?, p2=?, p3=?, athlete_id=? WHERE performance_id=?",
                   (performance.vo2max, performance.hr_max, performance.rf_max, performance.cadence_max, performance.ppo, performance.p1, performance.p2, performance.p3, performance.athlete_id, performance_id))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Performance not found")
    return {f"Performance no.{performance_id} updated successfully"}

@router.delete('/delete/{performance_id}')
def delete_performance(performance_id: int, db: sqlite3.Connection = Depends(get_db), current_user=Depends(get_current_user)):
    """Supprime une performance de la base de données.

    Args:
        performance_id (int): Identifiant de la performance à supprimer
        db (sqlite3.Connection): Connexion à la base de données
        current_user (dict): Utilisateur actuellement connecté

    Returns:
        dict: Message de confirmation avec l'ID de la performance supprimée

    Raises:
        HTTPException 401: Si l'utilisateur n'a pas les droits nécessaires (role coach ou admin)
        HTTPException 404: Si la performance n'est pas trouvée dans la base de données
    """
    cursor = db.cursor()
    role=current_user["role"]
    if role not in ["coach", "admin"]:
        raise HTTPException(status_code=401, detail="You are not allowed to perform this action")
    cursor.execute("DELETE FROM performance WHERE performance_id=?", (performance_id,))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Performance not found")
    return {f"Performance no.{performance_id} deleted successfully"}

@router.get('/performances')
def get_performances(db: sqlite3.Connection = Depends(get_db), current_user=Depends(get_current_user)):
    """Récupère les performances selon le rôle de l'utilisateur.

    Pour les coachs et admins : récupère toutes les performances.
    Pour les athlètes : récupère uniquement leurs propres performances.

    Args:
        db (sqlite3.Connection): Connexion à la base de données
        current_user (dict): Utilisateur actuellement connecté

    Returns:
        list: Liste des performances selon les droits de l'utilisateur
            - Toutes les performances pour les coachs/admins
            - Performances personnelles pour les athlètes
    """
    cursor = db.cursor()
    role=current_user["role"]
    if role in ["coach", "admin"]:
        cursor.execute("SELECT * FROM performance")
        performances = cursor.fetchall()
        return performances
    else:
        query = f"""
            select * from performance p
            inner join user u on p.athlete_id = u.user_id
            where user_id = ?
        """
        cursor.execute(query, (current_user["user_id"],))
        performances = cursor.fetchall()
        return performances