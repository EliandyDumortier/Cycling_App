import streamlit as st





st.title("Vous allez vous déconnecter")

if "show_confirmation" not in st.session_state:
    st.session_state.show_confirmation = False
# if "authenticated" not in st.session_state:
#     st.session_state.authenticated = True
# if "token" not in st.session_state:
#     st.session_state.token = "some_token"

def show_confirmation():
    st.session_state.show_confirmation = True

def logout():
    st.session_state.authenticated = False
    st.session_state.token = None
    st.session_state.show_confirmation = False
    st.rerun()

def cancel_logout():
    st.session_state.show_confirmation = False
    st.rerun()

if not st.session_state.show_confirmation:
    st.button("Deconnexion", type="primary", on_click=show_confirmation)
else:
    # Afficher la confirmation
    st.error("Voulez vous vraiment vous déconnecter ???")
    col1, col2 = st.columns(2)
    with col1:
        st.button("Oui", type="primary", key="btn_yes", on_click=logout)
    with col2:
        st.button("Non", type="primary", key="btn_no", on_click=cancel_logout)

