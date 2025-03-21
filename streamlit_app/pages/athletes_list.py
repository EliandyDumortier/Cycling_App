import streamlit as st
from dotenv import load_dotenv
import os
import requests
import json


load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8501")


def get_athletes_from_api():
    url = f"{API_URL}/athletes/athletes"
    token = st.session_state.token
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {token}"
    }
        
    response = requests.get(url, headers=headers)
    return response    


def delete_athlete(athlete_id, athlete_name):
    # Demander confirmation avant de supprimer
    if st.session_state.get("confirm_delete", False):
        url = f"{API_URL}/athletes/delete/{athlete_id}"
        token = st.session_state.token
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.delete(url, headers=headers)
        
        # Réinitialiser l'état de confirmation
        st.session_state.confirm_delete = False
        st.session_state.athlete_to_delete = None
        
        return response
    return None


def create_athlete(athlete_data):
    url = f"{API_URL}/athletes/create"
    token = st.session_state.token
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.post(url, json=athlete_data, headers=headers)
    return response


if st.session_state.authenticated and st.session_state.role in ["admin", "coach"]:
    st.title("Gestion des athlètes")
    
    # Afficher le message de succès si présent
    if st.session_state.get("success_message"):
        st.success(st.session_state.success_message)
        # Effacer le message après l'affichage
        st.session_state.success_message = None
    
    # Ajouter un bouton pour créer un nouvel athlète
    if st.button("Ajouter un athlète"):
        st.session_state.show_athlete_form = True
    
    # Formulaire pour ajouter un athlète
    if st.session_state.get("show_athlete_form", False):
        with st.form("new_athlete_form"):
            st.subheader("Nouvel athlète")
            
            name = st.text_input("Nom")
            gender = st.selectbox("Genre", ["male", "female"])
            age = st.number_input("Âge", min_value=0, step=1)
            weight = st.number_input("Poids (kg)", min_value=0.0)
            height = st.number_input("Taille (m)", min_value=0.0)
            user_id = st.number_input("ID utilisateur", min_value=1, step=1)
            
            submitted = st.form_submit_button("Soumettre")
            
            if submitted:
                athlete_data = {
                    "name": name,
                    "gender": gender,
                    "age": age,
                    "weight": weight,
                    "height": height,
                    "user_id": user_id
                }
                
                response = create_athlete(athlete_data)
                
                if response.status_code == 200:
                    st.session_state.success_message = f"Athlète {name} créé avec succès!"
                    st.session_state.show_athlete_form = False
                    st.rerun()
                else:
                    st.error(f"Erreur lors de la création: {response.text}")
    
    # Dialogue de confirmation de suppression
    if st.session_state.get("confirm_delete", False):
        athlete_name = st.session_state.get("athlete_to_delete_name", "")
        athlete_id = st.session_state.get("athlete_to_delete", None)
        
        st.warning(f"Êtes-vous sûr de vouloir supprimer l'athlète {athlete_name} ?")
        col1, col2 = st.columns(2)
        
        if col1.button("Oui, supprimer"):
            delete_response = delete_athlete(athlete_id, athlete_name)
            if delete_response and delete_response.status_code == 200:
                st.session_state.success_message = f"Athlète {athlete_name} supprimé avec succès!"
                st.rerun()
            elif delete_response:
                st.error(f"Erreur lors de la suppression: {delete_response.text}")
        
        if col2.button("Annuler"):
            st.session_state.confirm_delete = False
            st.session_state.athlete_to_delete = None
            st.session_state.athlete_to_delete_name = None
            st.rerun()
    
    # Afficher les athlètes existants
    response = get_athletes_from_api()
    
    if response.status_code == 200:
        athletes = json.loads(response.text)
        
        # Créer l'en-tête du tableau
        cols = st.columns([1, 1, 1, 1, 1, 1, 1])
        headers = ["ID", "Nom", "Genre", "Âge", "Poids", "Taille", "Action"]
        
        for col, header in zip(cols, headers):
            col.write(f"**{header}**")
        
        st.divider()
        
        # Afficher chaque athlète avec un bouton de suppression
        for athlete in athletes:
            cols = st.columns([1, 1, 1, 1, 1, 1, 1])
            
            cols[0].write(athlete["athlete_id"])
            cols[1].write(athlete["name"])
            cols[2].write(athlete["gender"])
            cols[3].write(athlete["age"])
            cols[4].write(f"{athlete['weight']} kg")
            cols[5].write(f"{athlete['height']} m")
            
            if cols[6].button("🗑️", key=f"delete_{athlete['athlete_id']}"):
                st.session_state.confirm_delete = True
                st.session_state.athlete_to_delete = athlete['athlete_id']
                st.session_state.athlete_to_delete_name = athlete['name']
                st.rerun()
            
            st.divider()
    else:
        st.error(f"Erreur lors de la récupération des données: {response.text}")
