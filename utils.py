"""
Module utilitaire pour la gestion de l'authentification et de la sécurité.

Ce module fournit les fonctions et configurations nécessaires pour :
- La gestion des tokens JWT
- Le hachage des mots de passe
- L'authentification des utilisateurs
- La récupération de l'utilisateur courant
"""

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
import os
from typing import Annotated
from dotenv import load_dotenv
from jose import JWTError, jwt
from sqlite3 import Connection

load_dotenv()

# Configuration des variables d'environnement
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
SECRET_KEY = os.getenv("SECRET_KEY", None)
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Configuration du contexte de cryptage et OAuth2
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/user/auth")

db_dependency = Depends(get_db)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Crée un token JWT d'accès.

    Args:
        data (dict): Données à encoder dans le token
        expires_delta (timedelta, optional): Durée de validité du token.
            Si non spécifié, utilise ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        str: Token JWT encodé

    Note:
        Le token inclut automatiquement une date d'expiration (exp)
        basée sur le temps UTC actuel plus la durée de validité.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_password_hash(password: str) -> str:
    """Hash un mot de passe en utilisant bcrypt.

    Args:
        password (str): Mot de passe en clair

    Returns:
        str: Hash du mot de passe

    Note:
        Utilise l'algorithme bcrypt avec les paramètres définis
        dans bcrypt_context.
    """
    return bcrypt_context.hash(password)

async def authenticate(email: str, password: str, db: Connection) -> dict:
    """Authentifie un utilisateur avec son email et mot de passe.

    Args:
        email (str): Email de l'utilisateur
        password (str): Mot de passe en clair
        db (Connection): Connexion à la base de données

    Returns:
        dict: Données de l'utilisateur si l'authentification réussit
        False: Si l'authentification échoue

    Note:
        Vérifie l'existence de l'utilisateur et la correspondance
        du mot de passe avec le hash stocké.
    """
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM user WHERE email = ?", (email,))
        user = cursor.fetchone()

        if not user:
            return False

        if not bcrypt_context.verify(password, user["password"]):
            return False

        return user
    finally:
        cursor.close()

async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)],
    db: Connection = Depends(get_db)
) -> dict:
    """Récupère l'utilisateur courant à partir du token JWT.

    Args:
        token (str): Token JWT d'authentification
        db (Connection): Connexion à la base de données

    Returns:
        dict: Données de l'utilisateur courant

    Raises:
        HTTPException 401: Si le token est invalide ou expiré
        HTTPException 404: Si l'utilisateur n'est pas trouvé

    Note:
        - Décode le token JWT
        - Vérifie sa validité
        - Récupère l'utilisateur correspondant dans la base de données
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalide"
            )

        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM user WHERE email = ?", (email,))
            user = cursor.fetchone()

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Utilisateur non trouvé"
                )

            return user
        finally:
            cursor.close()

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Erreur de token : {str(e)}"
        )