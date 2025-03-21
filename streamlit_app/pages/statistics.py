import streamlit as st
from dotenv import load_dotenv
import os
import streamlit.components.v1 as components
import webbrowser

load_dotenv()

if 'authenticated' in st.session_state and st.session_state.authenticated:
    st.title("Rapport Power BI")
    
    # URL du rapport Power BI
    report_url = "https://app.powerbi.com/links/xXZpOaMJp0?ctid=a2e466aa-4f86-4545-b5b8-97da7c8febf3&pbi_source=linkShare"
    
    # Option 1: Afficher un bouton pour ouvrir le rapport dans une nouvelle fenêtre
    if st.button("Ouvrir le rapport Power BI dans une nouvelle fenêtre"):
        st.markdown(f"<a href='{report_url}' target='_blank'>Cliquez ici si la page ne s'ouvre pas automatiquement</a>", unsafe_allow_html=True)
        st.components.v1.html(
            f"""
            <script>
                window.open('{report_url}', '_blank');
            </script>
            """,
            height=0
        )
