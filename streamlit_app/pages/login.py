import streamlit as st
from dotenv import load_dotenv
import os
import requests
import re


load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "token" not in st.session_state:
    st.session_state.token = None
if "role" not in st.session_state : 
    st.session_state.role = None    


st.session_state.role = "coach"


def get_token_from_api(email_saisi, password_saisi):
    url = f"{API_URL}/user/auth"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'password',
        'username': email_saisi,
        'password': password_saisi,
    }
        
    response = requests.post(url, headers=headers, data=data)
    return response    


def valid_email(email):
    return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))


st.title("Connexion")

email = st.text_input("Email")
password = st.text_input("Mot de passe", type="password")

if st.button("Se connecter") : 
    if not valid_email(email) : 
        st.warning("Veuillez saisir un email valide")
    else :
        response = get_token_from_api(email, password)
        # st.write(response.status_code)
        if response.status_code != 200 : 
            st.warning("Accès refusé")
        else :
            st.warning("Accès autorisé")
            token = response.json()["access_token"]
            st.write("token d'acces : ", token)
            st.session_state.token = token
            st.session_state.authenticated = True
            st.rerun()










