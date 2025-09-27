import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/recommend"

# --- Controle de estado ---
if "page" not in st.session_state:
    st.session_state.page = "home"
if "results" not in st.session_state:
    st.session_state.results = []
if "current_product" not in st.session_state:
    st.session_state.current_product = None

# --- Página Inicial (Busca) ---
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align: center; color: #FF69B4;'>💆🏻‍♀️ Sistema de Recomendação Skincare 🫧</h1>", unsafe_allow_html=True)
    ingredient = st.text_input("Digite o produto:")

    if st.button("Buscar"):
        # 1️⃣ Buscar dados do produto digitado
        payload_produto = {"ingredient": ingredient, "only_self": True}  # Flag para retornar apenas o produto buscado
        response_produto = requests.post(API_URL, json=payload_produto)

        if response_produto.status_code == 200:
            produto_buscado_list = response_produto.json().get("results", [])
            if not produto_buscado_list:
                st.warning("Produto não encontrado na base.")
            else:
                produto_buscado = produto_buscado_list[0]

                # 2️⃣ Buscar produtos semelhantes
                payload_similares = {"ingredient": ingredient}
                response_similares = requests.post(API_URL, json=payload_similares)

                if response_similares.status_code == 200:
                    similares = response_similares.json().get("results", [])
                    # Remove o próprio produto caso esteja repetido
                    similares = [s for s in similares if s["name"] != produto_buscado["name"]]

                    # 3️⃣ Monta a lista final: produto buscado + similares
                    st.session_state.results = [produto_buscado] + similares
                    st.session_state.page = "lista"
                    st.rerun()
                else:
                    st.error(f"Erro ao buscar produtos semelhantes: {response_similares.status_code}")
        else:
            st.error(f"Erro ao buscar produto: {response_produto.status_code}")

# --- Lista de Produtos ---
elif st.session_state.page == "lista":
    st.subheader("Resultados da Busca")
    for r in st.session_state.results:
        if st.button(r["name"]):
            st.session_state.current_product = r
            st.session_state.page = "produto"
            st.rerun()
    if st.button("Voltar"):
        st.session_state.page = "home"
        st.rerun()

# --- Página do Produto ---
elif st.session_state.page == "produto":
    produto = st.session_state.current_product
    if produto:
        st.header(f"🧴 {produto['name']}")
        st.write(f"**Marca:** {produto.get('brand', 'Desconhecida')}")
        st.write(f"**Ingredientes:** {produto.get('ingredients', 'Não informado')}")

        st.markdown("---")
        st.subheader("Produtos Semelhantes (Conteúdo)")

        # Busca produtos semelhantes novamente
        payload = {"ingredient": produto["name"]}
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            resp_json = response.json()
            similares = resp_json.get("results", [])
            # Remove o próprio produto da lista de similares
            similares = [s for s in similares if s["name"] != produto["name"]]

            for s in similares:
                if st.button(s["name"]):
                    st.session_state.current_product = s
                    st.session_state.page = "produto"
                    st.rerun()

    if st.button("Voltar para lista"):
        st.session_state.page = "lista"
        st.rerun()
