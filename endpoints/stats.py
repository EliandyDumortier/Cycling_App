# Description: This file contains the endpoints for the stats of the athletes
from fastapi import APIRouter,Depends, HTTPException
from database import get_db
from utils import get_current_user
import sqlite3

router=APIRouter(prefix="/stats")

@router.get('/vo2max')
def vo2max(db: sqlite3.Connection = Depends(get_db)):
    """Récupère l'athlète ayant la plus haute consommation maximale d'oxygène (VO2max).

    Cette fonction permet d'identifier l'athlète ayant la meilleure capacité aérobie
    parmi tous les athlètes enregistrés dans la base de données.

    Args:
        db (sqlite3.Connection): Connexion à la base de données

    Returns:
        tuple: Un tuple contenant :
            - athlete_id (int): L'identifiant de l'athlète
            - name (str): Le nom de l'athlète
            - vo2max (float): La valeur maximale de VO2max enregistrée

    Note:
        Les résultats sont groupés par athlète pour éviter les doublons
        et seule la valeur maximale est retournée.
    """
    cursor = db.cursor()
    cursor.execute("SELECT athlete_id, name, MAX(vo2max) FROM performance group by athlete_id,name")
    return cursor.fetchone()

@router.get('/ppo')
def ppo(db: sqlite3.Connection = Depends(get_db)):
    """Récupère l'athlète ayant la plus haute puissance maximale (PPO - Peak Power Output).

    Cette fonction permet d'identifier l'athlète le plus puissant en termes
    de puissance maximale développée.

    Args:
        db (sqlite3.Connection): Connexion à la base de données

    Returns:
        tuple: Un tuple contenant :
            - athlete_id (int): L'identifiant de l'athlète
            - name (str): Le nom de l'athlète
            - ppo (float): La valeur maximale de PPO enregistrée

    Note:
        Les résultats sont groupés par athlète pour éviter les doublons
        et seule la valeur maximale est retournée.
    """
    cursor = db.cursor()
    cursor.execute("SELECT athlete_id, name, MAX(ppo) FROM performance group by athlete_id,name")
    return cursor.fetchone()

@router.get('/weightpower')
def weightpower(db: sqlite3.Connection = Depends(get_db)):
    """Récupère l'athlète ayant le meilleur rapport puissance/poids.

    Cette fonction permet d'identifier l'athlète ayant le meilleur ratio
    entre sa puissance maximale (PPO) et son poids, ce qui est un indicateur
    important de performance relative.

    Args:
        db (sqlite3.Connection): Connexion à la base de données

    Returns:
        tuple: Un tuple contenant :
            - athlete_id (int): L'identifiant de l'athlète
            - name (str): Le nom de l'athlète
            - power_to_weight (float): Le meilleur ratio puissance/poids calculé

    Note:
        Les résultats sont groupés par athlète pour éviter les doublons
        et seule la valeur maximale est retournée.
        Ce ratio est particulièrement pertinent pour comparer des athlètes
        de différentes catégories de poids.
    """
    cursor = db.cursor()
    cursor.execute("SELECT athlete_id, name, MAX(ppo/weight) FROM performance group by athlete_id,name")
    return cursor.fetchone()