from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from database import connexion
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
import os
from typing import Annotated
from dotenv import load_dotenv
from jose import JWTError, jwt




load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
SECRET_KEY = os.getenv("SECRET_KEY", None)
ALGORITHM = os.getenv("ALGORITHM", "HS256")


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # pour hasher le mot de passe 
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="user/auth")  # pour obtenir le token d'accès à l'API  

db_dependency = Depends(connexion)


# token d'acces
def create_acces_token(data : dict, expires_delta : timedelta = None) : 
    to_encode = data.copy
    if expires_delta : 
        expire = datetime.now() + expires_delta
    else : 
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# hash du mot de passe
def get_password_hash(password : str) : 
    return bcrypt_context.hash(password)


# authentification
async def authenticate(email : str, password : str, db = db_dependency) :
    user = db.Cursor().Execute(" SELECT * FROM user WHERE email = ? ", (email,)).fetchone()
    if not user : 
        return False
    if not bcrypt_context.verify(password, user.hashed_password) : 
        return False
    return user


# recuperer l'utilisateur courant
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], db = db_dependency) : 
    try : 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
        user = db.Cursor().Execute(" SELECT * FROM user WHERE email = ? ", (email,)).fetchone()
        if user is None : 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="email invalide")
        return user
    except JWTError : 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")






