from fastapi import APIRouter, Depends, HTTPException, status
from utils import create_acces_token, get_password_hash, authenticate, get_current_user, db_dependency
from typing import Annotated




app = APIRouter(prefix="/user")



@app.get("/auth/")
def login(email, password, db = db_dependency) : 
    user = authenticate(email, password, db = db_dependency)
    if not user : 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nom d'utilisateur ou mot de passe incorrect, veuillez corriger votre saisie", headers={"WWW-Authenticate": "Bearer"})
    token_data = {
        "sub" : user.email
    }
    acces_token = create_acces_token(data=token_data)
    return {"access_token": acces_token, "token_type": "bearer"}



@app.get("/users/")
def get_users() :
    pass




@app.post("/create_user/")
def create_user() :
    pass








