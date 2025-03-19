from fastapi import APIRouter, Depends, HTTPException, status
from utils import create_acces_token, get_password_hash, authenticate, get_current_user, db_dependency, bcrypt_context
from schemas import CreateUserRequest
import os
from dotenv import load_dotenv



load_dotenv()
COACH_VERIFICATION_CODE = os.getenv("COACH_VERIFICATION_CODE", None)


app = APIRouter(prefix="/user")



@app.get("/auth/")
def login(email, password, db = db_dependency) : 
    user = authenticate(email, password, db)
    if not user : 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nom d'utilisateur ou mot de passe incorrect, veuillez corriger votre saisie", headers={"WWW-Authenticate": "Bearer"})
    token_data = {
        "sub" : user.email
    }
    acces_token = create_acces_token(data=token_data)
    return {"access_token": acces_token, "token_type": "bearer"}



@app.get("/users/")
def get_users(db = db_dependency, current_user = Depends(get_current_user)) : 
    role = current_user.role
    if role == "admin" : 
        result = db.Cursor().Execute("SELECT * FROM user").fetchall()
        return result
    else :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Accès refusé, vous n'avez pas les droits nécessairespour accéder à cette ressource")



@app.post("/create_user/")
def create_user(create_user_request : CreateUserRequest, db = db_dependency) : 
    name = create_user_request.name
    email = create_user_request.email
    password = create_user_request.password
    password_confirmation = create_user_request.password_confirmation
    role = create_user_request.role
    if role == "coach" : 
        coach_verification_code = create_user_request.coach_verification_code
    
    if password != password_confirmation : 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Les mots de passes ne correspondent pas")
    
    if coach_verification_code != COACH_VERIFICATION_CODE :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Le code de vérification du coach est invalide")
    
    if password == password_confirmation and coach_verification_code == COACH_VERIFICATION_CODE : 
        hashed_password = bcrypt_context.hash(password)
        db.Cursor().Execute(f"""
            INSERT INTO user ('name', 'email', 'password', 'role')
            VALUES (?,?,?,?)""", (name, email, hashed_password, role))
        return {"message" : f"Utilisateur {name} créé avec succès !"}








