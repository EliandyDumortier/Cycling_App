"""
Module de gestion des requêtes SQL pour l'application de gestion de cyclisme.

Ce module fournit des fonctions utilitaires pour effectuer des opérations CRUD
(Create, Read, Update, Delete) sur la base de données SQLite.
Toutes les fonctions gèrent automatiquement la connexion et sa fermeture.
"""

from sqlite3 import Connection
from database import get_db
import json

def insert_data(table_name: str, data: tuple[str|int|float|bool], con: Connection = get_db()):
    """Insère de nouvelles données dans une table spécifiée.

    Args:
        table_name (str): Nom de la table dans laquelle insérer les données
        data (tuple): Tuple contenant les valeurs à insérer. Les types acceptés sont :
            - str: Pour les chaînes de caractères
            - int: Pour les nombres entiers
            - float: Pour les nombres décimaux
            - bool: Pour les valeurs booléennes
        con (Connection, optional): Connexion à la base de données.
            Defaults to get_db().

    Note:
        - La fonction récupère automatiquement les noms des colonnes de la table
        - La première colonne (généralement l'ID) est exclue car auto-incrémentée
        - La connexion est automatiquement fermée après l'opération

    Raises:
        Exception: Si une erreur survient pendant l'insertion des données

    Example:
        >>> values = ("4650", "180", "200", 360, 134, 286, 333, "sub_1")
        >>> insert_data("performance", values)
        "INSERT INTO performance(col1, col2, ...) VALUES (4650, 180, ...)"
        "SUCCES"
    """
    connexion = next(con)
    try:
        cursor = connexion.cursor()
        table_info = cursor.execute(f"PRAGMA table_info({table_name});").fetchall()
        columns = tuple([c[1] for c in table_info][1:])
        query = f"INSERT INTO {table_name}{columns} VALUES {data}"
        print(query)
        cursor.execute(query)
        connexion.commit()
        print("SUCCES")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        con.close()

def update_data(table_name: str, column_name: str, new_value: str|int|float|bool, id_to_modify: int, con: Connection = get_db()):
    """Met à jour une valeur spécifique dans une table.

    Args:
        table_name (str): Nom de la table à modifier
        column_name (str): Nom de la colonne à modifier
        new_value (str|int|float|bool): Nouvelle valeur à insérer
        id_to_modify (int): ID de l'enregistrement à modifier
        con (Connection, optional): Connexion à la base de données.
            Defaults to get_db().

    Note:
        - La fonction utilise l'ID comme critère de modification
        - La connexion est automatiquement fermée après l'opération

    Raises:
        Exception: Si une erreur survient pendant la mise à jour

    Example:
        >>> update_data("athlete", "name", "John Doe", 1)
        # Met à jour le nom de l'athlète ayant l'ID 1
    """
    connexion = next(con)
    try:
        cursor = connexion.cursor()
        query = f"UPDATE {table_name} SET {column_name} = {new_value} WHERE id = {id_to_modify}"
        cursor.execute(query)
        connexion.commit()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        con.close()

def delete_data(table_name: str, id_to_delete: int, con: Connection = get_db()):
    """Supprime un enregistrement d'une table spécifiée.

    Args:
        table_name (str): Nom de la table dans laquelle effectuer la suppression
        id_to_delete (int): ID de l'enregistrement à supprimer
        con (Connection, optional): Connexion à la base de données.
            Defaults to get_db().

    Note:
        - La fonction utilise l'ID comme critère de suppression
        - La connexion est automatiquement fermée après l'opération
        - Cette opération est irréversible

    Raises:
        Exception: Si une erreur survient pendant la suppression

    Example:
        >>> delete_data("performance", 1)
        # Supprime la performance ayant l'ID 1
    """
    connexion = next(con)
    try:
        cursor = connexion.cursor()
        query = f"DELETE FROM {table_name} WHERE id = {id_to_delete}"
        cursor.execute(query)
        connexion.commit()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        con.close()

if __name__ == "__main__":
    """
    Point d'entrée du script pour les tests.
    Exemple d'insertion de données de performance.
    """
    values = ("4650", "180", "200", 360, 134, 286, 333, "sub_1")
    insert_data("performance", values)