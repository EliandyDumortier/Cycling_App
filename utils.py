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

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
SECRET_KEY = os.getenv("SECRET_KEY", "secret-fallback")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/user/auth")

db_dependency = Depends(get_db)

# Token d'accès
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Hash du mot de passe
def get_password_hash(password: str):
    return bcrypt_context.hash(password)


# Authentification
async def authenticate(email: str, password: str, db: Connection):
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


# Récupérer l'utilisateur courant
async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)], 
    db: Connection = Depends(get_db)
):
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
