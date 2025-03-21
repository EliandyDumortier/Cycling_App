"""
Module de peuplement de la base de données pour l'application de gestion de cyclisme.

Ce script permet de générer des données de test pour la base de données,
incluant des utilisateurs (athlètes et coachs), des profils d'athlètes
et leurs performances associées.

Les données générées sont aléatoires mais réalistes pour simuler un
environnement de production.
"""

import sqlite3
import random

def populate_database(db_path="cycling.db"):
    """Peuple la base de données avec des données de test.

    Cette fonction crée :
        - 19 nouveaux athlètes
        - 1 nouveau coach
        - Des profils d'athlètes avec données physiologiques
        - Des performances aléatoires pour chaque athlète

    Args:
        db_path (str, optional): Chemin vers le fichier de base de données.
            Defaults to "cycling.db".

    Returns:
        tuple: Un tuple contenant :
            - nombre d'utilisateurs créés
            - nombre d'athlètes créés
            - nombre total de performances générées

    Note:
        Les données générées suivent ces paramètres :
        - Âge des athlètes : 18-40 ans
        - Poids : 50-90 kg
        - Taille : 1.50-2.00 m
        - VO2max : 45-65 ml/kg/min
        - FC max : 160-200 bpm
        - Cadence max : 80-110 rpm
        - PPO (Peak Power Output) : 280-400 watts
        - P1 (Puissance zone 1) : 180-300 watts
        - P2 (Puissance zone 2) : 160-280 watts
        - P3 (Puissance zone 3) : 140-260 watts
    """
    # Ensure proper database connection
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Insert 19 new athletes and 1 new coach into the user table
        new_users = [
            (f"Athlete {i}", f"athlete{i}@mail.com", "$2b$12$dummyhash", "athlete")
            for i in range(2, 21)
        ] + [("Coach2", "coach2@mail.com", "$2b$12$dummyhash", "coach")]

        cursor.executemany(
            "INSERT INTO user (name, email, password, role) VALUES (?, ?, ?, ?)",
            new_users
        )
        conn.commit()

        # Retrieve all athlete users (excluding coaches)
        cursor.execute("SELECT user_id, name FROM user WHERE role = 'athlete'")
        athlete_users = cursor.fetchall()

        # Insert all athletes into the athlete table
        new_athletes = [
            (name, random.choice(["male", "female"]),
             random.randint(18, 40),
             round(random.uniform(50, 90), 2),
             round(random.uniform(1.50, 2.00), 2),
             user_id)
            for user_id, name in athlete_users
        ]

        cursor.executemany(
            """INSERT INTO athlete
               (name, gender, age, weight, height, user_id)
               VALUES (?, ?, ?, ?, ?, ?)""",
            new_athletes
        )
        conn.commit()

        # Retrieve all athlete IDs
        cursor.execute("SELECT athlete_id FROM athlete")
        athlete_ids = [row[0] for row in cursor.fetchall()]

        def generate_performance_data(athlete_id):
            """Génère des données de performance aléatoires pour un athlète.

            Args:
                athlete_id (int): ID de l'athlète

            Returns:
                tuple: Données de performance incluant :
                    - vo2max (float)
                    - hr_max (int)
                    - cadence_max (int)
                    - ppo (int)
                    - p1 (int)
                    - p2 (int)
                    - p3 (int)
                    - athlete_id (int)
            """
            return (
                round(random.uniform(45, 65), 2),  # vo2max
                random.randint(160, 200),          # hr_max
                random.randint(80, 110),           # cadence_max
                random.randint(280, 400),          # ppo
                random.randint(180, 300),          # p1
                random.randint(160, 280),          # p2
                random.randint(140, 260),          # p3
                athlete_id
            )

        # Generate 0-5 performance records per athlete
        performance_data = []
        for athlete_id in athlete_ids:
            num_performances = random.randint(0, 5)
            for _ in range(num_performances):
                performance_data.append(generate_performance_data(athlete_id))

        # Insert performance data
        cursor.executemany(
            """INSERT INTO performance
               (vo2max, hr_max, cadence_max, ppo, p1, p2, p3, athlete_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            performance_data
        )

        conn.commit()

    return len(new_users), len(new_athletes), len(performance_data)

if __name__ == "__main__":
    """
    Point d'entrée du script.
    Exécute le peuplement de la base de données et affiche les résultats.
    """
    users, athletes, performances = populate_database()
    print(f"""
    Base de données peuplée avec succès :
    - {users} nouveaux utilisateurs créés
    - {athletes} nouveaux athlètes créés
    - {performances} performances générées
    """)