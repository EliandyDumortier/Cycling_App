from pydantic import BaseModel, Field, EmailStr
from typing import Literal



class CreateUserRequest(BaseModel) : 
    name : str = Field(description="Nom et prénom")
    email : EmailStr = Field(description="Adresse email")
    password : str = Field(min_length=8, description="Votre mot de passe. Longueur monimale de 8 caractères")
    password_confirmation : str = Field(description="Confirmation du mot de passe. Longueur monimale de 8 caractères")
    role: Literal["coach", "athlete"] = Field(...)
    if role == "coach" : 
        coach_verification_code : str = Field(description="Votre code de vérification de coach")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jean MOMO",
                "email": "mon_email@domaine.com",
                "password": "azerty12",
                "password_confirmation": "azerty12",
                "role" : "athlete"
            }
        }        








