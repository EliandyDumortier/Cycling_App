import streamlit as st
from dotenv import load_dotenv
import os
import requests


load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8501")



def get_token_from_api():
    url = f"{API_URL}/athletes/athletes"
    token = st.session_state.token
    headers = {
        "accept" : "application/json",
        "Content-Type" : "application/x-www-form-urlencoded",
        "Authorization" : f"Bearer {token}"
    }
        
    response = requests.get(url, headers=headers)
    return response    


if st.session_state.authenticated and st.session_state.role in ["admin", "coach"] :
    response = get_token_from_api()
    st.write(response.text)

