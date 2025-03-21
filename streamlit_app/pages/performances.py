import streamlit as st
from dotenv import load_dotenv
import os
import requests
import json
import time


load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8501")


def get_performances_from_api():
    url = f"{API_URL}/performances/performances"
    token = st.session_state.token
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {token}"
    }
        
    response = requests.get(url, headers=headers)
    return response    


def delete_performance(performance_id):
    url = f"{API_URL}/performances/delete/{performance_id}"
    token = st.session_state.token
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.delete(url, headers=headers)
    return response


def create_performance(performance_data):
    url = f"{API_URL}/performances/create"
    token = st.session_state.token
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.post(url, json=performance_data, headers=headers)
    return response


if st.session_state.authenticated and st.session_state.role in ["admin", "coach"]:
    st.title("Gestion des performances")
    
    # Ajouter un bouton pour créer une nouvelle performance
    if st.button("Ajouter une performance"):
        st.session_state.show_form = True
    
    # Formulaire pour ajouter une performance
    if st.session_state.get("show_form", False):
        with st.form("new_performance_form"):
            st.subheader("Nouvelle performance")
            
            vo2max = st.number_input("VO2 Max", min_value=0.0)
            hr_max = st.number_input("HR Max", min_value=0.0)
            rf_max = st.number_input("RF Max", min_value=0.0)
            cadence_max = st.number_input("Cadence Max", min_value=0.0)
            ppo = st.number_input("PPO", min_value=0.0)
            p1 = st.number_input("P1", min_value=0.0)
            p2 = st.number_input("P2", min_value=0.0)
            p3 = st.number_input("P3", min_value=0.0)
            athlete_id = st.number_input("ID de l'athlète", min_value=1, step=1)
            
            submitted = st.form_submit_button("Soumettre")
            
            if submitted:
                performance_data = {
                    "vo2max": vo2max,
                    "hr_max": hr_max,
                    "rf_max": rf_max,
                    "cadence_max": cadence_max,
                    "ppo": ppo,
                    "p1": p1,
                    "p2": p2,
                    "p3": p3,
                    "athlete_id": athlete_id
                }
                
                response = create_performance(performance_data)
                
                if response.status_code == 200:
                    st.success("Performance créée avec succès!")
                    st.session_state.show_form = False
                    st.rerun()
                else:
                    st.error(f"Erreur lors de la création: {response.text}")
    
    # Afficher les performances existantes
    response = get_performances_from_api()
    
    if response.status_code == 200:
        performances = json.loads(response.text)
        
        # Créer l'en-tête du tableau
        cols = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1])
        headers = ["athlete_id", "VO2 Max", "HR Max", "Cadence", "PPO", "P1", "P2", "P3", "Action"]
        
        for col, header in zip(cols, headers):
            col.write(f"**{header}**")
        
        st.divider()
        
        # Afficher chaque performance avec un bouton de suppression
        for perf in performances:
            cols = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1])
            
            cols[0].write(perf["athlete_id"])
            cols[1].write(perf["vo2max"])
            cols[2].write(perf["hr_max"])
            cols[3].write(perf["cadence_max"])
            cols[4].write(perf["ppo"])
            cols[5].write(perf["p1"])
            cols[6].write(perf["p2"])
            cols[7].write(perf["p3"])
            
            if cols[8].button("🗑️", key=f"delete_{perf['performance_id']}"):
                delete_response = delete_performance(perf['performance_id'])
                if delete_response.status_code == 200:
                    st.success(f"Performance supprimée avec succès!")
                    time.sleep(3)
                    st.rerun()
                else:
                    st.error(f"Erreur lors de la suppression: {delete_response.text}")
            
            st.divider()
    else:
        st.error(f"Erreur lors de la récupération des données: {response.text}")
