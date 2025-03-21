import streamlit as st



# st.title("Cycling app")
st.title("Bienvenue sur l'API de Gestion des Performances des Cyclistes")


st.image("https://simplonline.co/_next/image?url=https%3A%2F%2Fsimplonline-v3-prod.s3.eu-west-3.amazonaws.com%2Fmedia%2Fimage%2Fjpg%2Fpiste-67d8881022189387476191.jpg&w=1280&q=75", caption="Performance des Cyclistes")


st.write("""
Cette application permet de gérer et d'analyser les performances des cyclistes professionnels. Elle offre une API RESTful pour enregistrer les données des athlètes et consulter des statistiques détaillées sur leurs performances.

### Fonctionnalités principales :
- **Authentification sécurisée** : Inscription et connexion des utilisateurs via un système de tokens JWT.
- **Gestion des athlètes** : Ajout, modification et suppression des informations des cyclistes (Nom, Âge, VO2max, etc.).
- **Suivi des performances** : Enregistrement des données de performance (Puissance moyenne, rapport poids/puissance, etc.).
- **Statistiques avancées** : Accès aux athlètes les plus puissants, à ceux avec la VO2max la plus élevée, et bien plus.

Grâce à cette interface, vous pourrez visualiser les performances des cyclistes et suivre leur évolution au fil du temps.
""")
