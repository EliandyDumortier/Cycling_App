"""
Module de définition des schémas de données pour l'application de gestion de cyclisme.

Ce module utilise Pydantic pour définir les modèles de données et assurer
la validation des données entrantes. Il définit les structures de données
attendues pour les différentes opérations de l'API.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Literal

class CreateUserRequest(BaseModel):
    """Schéma de données pour la création d'un nouvel utilisateur.

    Ce modèle définit la structure et les validations pour les données
    nécessaires à la création d'un nouveau compte utilisateur.

    Attributes:
        name (str): Nom et prénom de l'utilisateur
        email (EmailStr): Adresse email valide de l'utilisateur
        password (str): Mot de passe avec une longueur minimale de 8 caractères
        password_confirmation (str): Confirmation du mot de passe
        role (str): Rôle de l'utilisateur (coach ou athlete)

    Validation:
        - L'email doit être dans un format valide
        - Le mot de passe doit faire au moins 8 caractères
        - Le rôle doit être soit "coach" soit "athlete"

    Example:
        >>> user_data = {
        ...     "name": "Jean MOMO",
        ...     "email": "mon_email@domaine.com",
        ...     "password": "azerty12",
        ...     "password_confirmation": "azerty12",
        ...     "role": "athlete"
        ... }
        >>> user = CreateUserRequest(**user_data)
    """

    name: str = Field(
        description="Nom et prénom",
        example="Jean MOMO"
    )

    email: EmailStr = Field(
        description="Adresse email",
        example="mon_email@domaine.com"
    )

    password: str = Field(
        min_length=8,
        description="Votre mot de passe. Longueur minimale de 8 caractères",
        example="azerty12"
    )

    password_confirmation: str = Field(
        description="Confirmation du mot de passe. Longueur minimale de 8 caractères",
        example="azerty12"
    )

    role: str = Field(
        description="coach, athlete",
        example="athlete"
    )

    class Config:
        """Configuration du schéma avec un exemple complet.

        Cette configuration fournit un exemple de données valides
        pour la documentation automatique de l'API.
        """
        json_schema_extra = {
            "example": {
                "name": "Jean MOMO",
                "email": "mon_email@domaine.com",
                "password": "azerty12",
                "password_confirmation": "azerty12",
                "role": "athlete"
            }
        }

    def validate_passwords_match(self):
        """Valide que les deux mots de passe correspondent.

        Returns:
            bool: True si les mots de passe correspondent

        Raises:
            ValueError: Si les mots de passe ne correspondent pas
        """
        if self.password != self.password_confirmation:
            raise ValueError("Les mots de passe ne correspondent pas")
        return True

    def validate_role(self):
        """Valide que le rôle est autorisé.

        Returns:
            bool: True si le rôle est valide

        Raises:
            ValueError: Si le rôle n'est pas "coach" ou "athlete"
        """
        if self.role not in ["coach", "athlete"]:
            raise ValueError("Le rôle doit être 'coach' ou 'athlete'")
        return True