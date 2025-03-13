import streamlit as st
import requests

API_URL = "http://user_service:8001"

st.title("📥 Interface Utilisateur - Insertion CSV Adaptée")

text = st.text_area("Entrez le texte :", height=100)
language = st.text_input("Langue :", value="French")

if st.button("Envoyer"):
    response = requests.post(f"{API_URL}/insert", json={"text": text, "language": language})
    if response.status_code == 200:
        st.success("✅ Donnée insérée avec succès !")
    else:
        st.error(f"❌ Erreur {response.status_code}")
