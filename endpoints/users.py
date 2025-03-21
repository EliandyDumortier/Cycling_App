from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlite3 import Connection
from utils import create_access_token, authenticate, get_current_user, bcrypt_context
from schemas import CreateUserRequest
from database import get_db
import os
from dotenv import load_dotenv
import sqlite3
from fastapi.security import OAuth2PasswordRequestForm

load_dotenv()

router = APIRouter(prefix="/user")

@router.post("/auth")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Connection = Depends(get_db)):
    """Authentifie un utilisateur et génère un token d'accès.

    Args:
        form_data (OAuth2PasswordRequestForm): Formulaire contenant les identifiants de connexion
            - username: Email de l'utilisateur
            - password: Mot de passe de l'utilisateur
        db (Connection): Connexion à la base de données

    Returns:
        dict: Dictionnaire contenant :
            - access_token (str): Token JWT d'authentification
            - token_type (str): Type de token (bearer)

    Raises:
        HTTPException 401: Si les identifiants sont incorrects
        HTTPException 500: En cas d'erreur serveur
    """
    try:
        user = await authenticate(form_data.username, form_data.password, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants incorrects")

        token_data = {"sub": user["email"]}
        access_token = create_access_token(token_data)

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

@router.get("/users")
async def get_users(db: Connection = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Récupère la liste de tous les utilisateurs.

    Cette route est accessible uniquement aux administrateurs et aux coachs.

    Args:
        db (Connection): Connexion à la base de données
        current_user (dict): Utilisateur actuellement connecté

    Returns:
        dict: Dictionnaire contenant la liste des utilisateurs avec leurs informations :
            - user_id: Identifiant de l'utilisateur
            - name: Nom de l'utilisateur
            - email: Email de l'utilisateur
            - role: Rôle de l'utilisateur

    Raises:
        HTTPException 403: Si l'utilisateur n'a pas les droits nécessaires
        HTTPException 500: En cas d'erreur de base de données
    """
    try:
        if current_user["role"] != "admin" and current_user["role"] != "coach" :
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès refusé"
            )

        cursor = db.cursor()
        cursor.execute("SELECT user_id, name, email, role FROM user")
        users = cursor.fetchall()
        cursor.close()

        return {"users": users}

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Erreur base de données: {str(e)}")

@router.post("/create_athlete")
async def create_athlete(create_user_request: CreateUserRequest, db: Connection = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Crée un nouveau compte athlète.

    Cette route est accessible uniquement aux coachs.

    Args:
        create_user_request (CreateUserRequest): Données de création du compte athlète
            - name: Nom de l'athlète
            - email: Email de l'athlète
            - password: Mot de passe
            - password_confirmation: Confirmation du mot de passe
            - role: Rôle (doit être "athlete")
        db (Connection): Connexion à la base de données
        current_user (dict): Utilisateur actuellement connecté

    Returns:
        dict: Message de confirmation de création

    Raises:
        HTTPException 400: Si les mots de passe ne correspondent pas ou si l'email existe déjà
        HTTPException 403: Si l'utilisateur n'est pas un coach
        HTTPException 500: En cas d'erreur serveur
    """
    cursor = db.cursor()
    try:
        if create_user_request.password != create_user_request.password_confirmation:
            raise HTTPException(status_code=400, detail="Les mots de passe ne correspondent pas")

        if current_user.role == "coach" :
            cursor.execute(
                "SELECT email FROM user WHERE email = ?",
                (create_user_request.email,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Email déjà utilisé")

            hashed_password = bcrypt_context.hash(create_user_request.password)

            cursor.execute(
                """INSERT INTO user (name, email, password, role)
                VALUES (?, ?, ?, ?)""",
                (create_user_request.name, create_user_request.email, hashed_password, create_user_request.role))
            db.commit()

            return {"message": "Utilisateur créé avec succès"}
        else:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="accès refusé")

    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Erreur d'intégrité: {str(e)}")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")
    finally:
        cursor.close()

@router.post("/create_coach")
async def create_coach(create_user_request: CreateUserRequest, db: Connection = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Crée un nouveau compte coach.

    Cette route est accessible uniquement aux administrateurs.

    Args:
        create_user_request (CreateUserRequest): Données de création du compte coach
            - name: Nom du coach
            - email: Email du coach
            - password: Mot de passe
            - password_confirmation: Confirmation du mot de passe
            - role: Rôle (doit être "coach")
        db (Connection): Connexion à la base de données
        current_user (dict): Utilisateur actuellement connecté

    Returns:
        dict: Message de confirmation de création

    Raises:
        HTTPException 400: Si les mots de passe ne correspondent pas ou si l'email existe déjà
        HTTPException 403: Si l'utilisateur n'est pas un administrateur
        HTTPException 500: En cas d'erreur serveur
    """
    cursor = db.cursor()
    try:
        if create_user_request.password != create_user_request.password_confirmation:
            raise HTTPException(status_code=400, detail="Les mots de passe ne correspondent pas")

        if current_user.role == "admin" and create_user_request.role == "coach" :
            cursor.execute(
                "SELECT email FROM user WHERE email = ?",
                (create_user_request.email,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Email déjà utilisé")

            hashed_password = bcrypt_context.hash(create_user_request.password)

            cursor.execute(
                """INSERT INTO user (name, email, password, role)
                VALUES (?, ?, ?, ?)""",
                (create_user_request.name, create_user_request.email, hashed_password, create_user_request.role))
            db.commit()

            return {"message": "Utilisateur créé avec succès"}
        else:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="accès refusé")

    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Erreur d'intégrité: {str(e)}")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")
    finally:
        cursor.close()