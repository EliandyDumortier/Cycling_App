import streamlit as st
from dotenv import load_dotenv
import os
import requests


load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8501/")

print(API_URL)

if st.session_state.authenticated : 
    pass
