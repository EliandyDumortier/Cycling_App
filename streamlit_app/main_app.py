import streamlit as st
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", None)
ALGORITHM = os.getenv("ALGORITHM", "HS256")


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False



current_user = "coach"

pages = [
    st.Page("pages/home.py", title="Accueil"),
    st.Page("pages/login.py", title="Connexion"),
]

if st.session_state.authenticated : 
    if current_user  == "admin" : 
        pages = [
            st.Page("pages/home.py", title="Accueil"),
            st.Page("pages/athletes_list.py", title="Liste des athlètes"),
            st.Page("pages/performances.py", title="Performances"),
            st.Page("pages/statistics.py", title="Statistiques"),
            st.Page("pages/logout.py", title="Deconnexion"),
        ]

    elif current_user == "coach" : 
        pages = [
            st.Page("pages/home.py", title="Accueil"),
            st.Page("pages/athletes_list.py", title="Liste des athlètes"),
            st.Page("pages/performances.py", title="Performances"),
            st.Page("pages/statistics.py", title="Statistiques"),
            st.Page("pages/logout.py", title="Deconnexion")
        ]

    elif current_user == "athlete" : 
        pages = [
            st.Page("pages/home.py", title="Accueil"),
            st.Page("pages/performances.py", title="Performances"),
            st.Page("pages/statistics.py", title="Statistiques"),
            st.Page("pages/logout.py", title="Deconnexion")
        ]



pg = st.navigation(pages)
pg.run()

