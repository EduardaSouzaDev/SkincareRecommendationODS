import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/recommend"

st.title("💆🏻‍♀️ Sistema de Recomendação Skincare 🫧⋆｡˚")

ingredient = st.text_input("Digite um produto:")

if st.button("Recomendar"):
    payload = {"ingredient": ingredient}
    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        results = response.json()["results"]
        st.subheader("Resultados:")
        for r in results:
            st.write(f"🧴**{r['name']}** - Marca: {r['brand']} ")
            st.write(f"Ingredientes: {r['ingredients']}")
            st.markdown("---")
    else:
        st.error("Erro ao consultar API")
