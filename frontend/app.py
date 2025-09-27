import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/recommend"



# Controle de navegação
if "page" not in st.session_state:
    st.session_state.page = "home"
    

# Armazenar resultados da API
if "results" not in st.session_state:
    st.session_state.results = None

# Página Inicial
if st.session_state.page == "home":
    st.title("💆🏻‍♀️ Sistema de Recomendação Skincare 🫧⋆｡˚")
    ingredient = st.text_input("Digite um produto:")

    if st.button("Buscar"):
        payload = {"ingredient": ingredient}
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            resp_json = response.json()
            if resp_json.get("results"):  
                # Salva resultados no estado
                st.session_state.results = resp_json["results"]
                # Vai para página do produto
                st.session_state.page = "produto"
                st.rerun()
            elif resp_json.get("error"):
                st.warning(resp_json["error"])
            else:
                st.warning("Nenhum resultado retornado.")
        else:
            st.error(f"Erro ao consultar API: {response.status_code}")

# Página do Produto
elif st.session_state.page == "produto":
    st.title("Página do Produto")

    if st.session_state.results:
        st.subheader("Recomendados:")
        for r in st.session_state.results:
            st.write(f"🧴 **{r['name']}** - Marca: {r['brand']}")
            st.write(f"Ingredientes: {r['ingredients']}")
            st.markdown("---")

    if st.button("Voltar"):
        st.session_state.page = "home"
        st.rerun()
