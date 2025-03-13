import streamlit as st
import requests
import pandas as pd

API_URL = "http://admin_service:8002"

st.title("🔧 Interface Administrateur - Gestion des Données CSV")

if st.button("Afficher toutes les données"):
    response = requests.get(f"{API_URL}/get-all")
    if response.status_code == 200:
        data = response.json()["results"]
        df = pd.DataFrame([
            {
                "ID": d["_id"],
                "Texte": d["_source"]["text"],
                "Langue": d["_source"]["language"],
                "Créé le": d["_source"].get("created_at", "N/A")
            }
            for d in data
        ])
        st.dataframe(df)
    else:
        st.error(f"❌ Erreur {response.status_code}")

st.divider()

st.header("✏️ Mettre à jour une donnée")
doc_id = st.text_input("ID du document à mettre à jour:")
new_text = st.text_area("Nouveau texte :", height=100)
new_language = st.text_input("Nouvelle langue :")

if st.button("Mettre à jour"):
    if doc_id and new_text and new_language:
        response = requests.put(f"{API_URL}/update", json={"id": doc_id, "text": new_text, "language": new_language})
        if response.status_code == 200:
            st.success("✅ Donnée mise à jour avec succès !")
        else:
            st.error(f"❌ Erreur {response.status_code}")
    else:
        st.warning("⚠️ Tous les champs doivent être remplis.")
