import sqlite3
from contextlib import contextmanager

"""
Module de gestion de la base de données pour l'application de cyclisme.
Ce module fournit les fonctions nécessaires pour initialiser et gérer
la connexion à la base de données SQLite.
"""

def get_db():
    """Crée et retourne une connexion à la base de données.

    Returns:
        sqlite3.Connection: Un objet de connexion à la base de données avec
        row_factory configuré pour retourner des objets de type sqlite3.Row

    Note:
        La connexion est automatiquement fermée après utilisation grâce
        au mot-clé yield.
    """
    connexion = sqlite3.connect("cycling.db")
    connexion.row_factory = sqlite3.Row
    try:
        yield connexion
    finally:
        connexion.close()

def init_db():
    """Initialise la structure de la base de données.

    Cette fonction crée les tables nécessaires si elles n'existent pas déjà :
        - user : Table des utilisateurs (athlètes, coachs, admin)
        - athlete : Table des informations spécifiques aux athlètes
        - performance : Table des performances des athlètes

    Tables créées:
        user:
            - user_id (INTEGER): Clé primaire auto-incrémentée
            - name (TEXT): Nom de l'utilisateur
            - email (TEXT): Email unique de l'utilisateur
            - password (TEXT): Mot de passe hashé
            - role (TEXT): Rôle de l'utilisateur (default: "athlete")

        athlete:
            - athlete_id (INTEGER): Clé primaire auto-incrémentée
            - name (TEXT): Nom de l'athlète
            - gender (TEXT): Genre de l'athlète
            - age (INTEGER): Âge de l'athlète
            - weight (REAL): Poids de l'athlète
            - height (REAL): Taille de l'athlète
            - user_id (INTEGER): Clé étrangère vers la table user

        performance:
            - performance_id (INTEGER): Clé primaire auto-incrémentée
            - vo2max (REAL): Consommation maximale d'oxygène
            - hr_max (REAL): Fréquence cardiaque maximale
            - cadence_max (REAL): Cadence maximale
            - ppo (REAL): Puissance maximale
            - p1 (REAL): Puissance zone 1
            - p2 (REAL): Puissance zone 2
            - p3 (REAL): Puissance zone 3
            - athlete_id (INTEGER): Clé étrangère vers la table athlete
    """
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
    """Gestionnaire de contexte pour la connexion à la base de données.

    Cette fonction utilise le décorateur contextmanager pour fournir une
    connexion à la base de données dans un contexte "with", assurant ainsi
    la fermeture automatique de la connexion.

    Yields:
        sqlite3.Connection: Un objet de connexion à la base de données configuré
        avec row_factory pour retourner des objets de type sqlite3.Row

    Note:
        L'option check_same_thread=False est utilisée pour permettre l'accès
        à la connexion depuis différents threads.
    """
    conn = sqlite3.connect("cycling.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def get_db():
    """Fournit une connexion à la base de données utilisant le gestionnaire de contexte.

    Cette fonction utilise db_connection pour fournir une connexion sécurisée
    qui sera automatiquement fermée après utilisation.

    Yields:
        sqlite3.Connection: Un objet de connexion à la base de données
    """
    with db_connection() as conn:
        yield conn

if __name__ == "__main__":
    # Initialisation de la base de données si le script est exécuté directement
    init_db()