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
if "ingredient" not in st.session_state:
    st.session_state.ingredient = ""
# --- Container fixo no topo (título + busca) ---
header_container = st.container()
with header_container:
    st.markdown("<h1 style='text-align:center; color:#FF69B4;'>💆🏻‍♀ Sistema de Recomendação Skincare 🫧</h1>", unsafe_allow_html=True)
    ingredient_input = st.text_input("Digite o produto:", value = None)
    if st.button("Buscar"):
        st.session_state.ingredient = ingredient_input
        #st.session_state.ingredient = ""
        print(st.session_state.ingredient)
        # Busca o produto buscado
        payload_produto = {"ingredient": ingredient_input, "only_self": True}
        response_produto = requests.post(API_URL, json=payload_produto)
        if response_produto.status_code == 200:
            produto_buscado_list = response_produto.json().get("results", [])
            if not produto_buscado_list:
                st.warning("Produto não encontrado.")
                st.session_state.page = "home"
            else:
                produto_buscado = produto_buscado_list[0]

                # Busca produtos semelhantes
                payload_similares = {"ingredient": ingredient_input}
                response_similares = requests.post(API_URL, json=payload_similares)
                if response_similares.status_code == 200:
                    similares = response_similares.json().get("results", [])
                    # Remove duplicata do produto buscado
                    similares = [s for s in similares if s["name"] != produto_buscado["name"]]
                    st.session_state.results = [produto_buscado] + similares
                    st.session_state.page = "lista"
                   # del st.session_state.ingredient
                    print(st.session_state.ingredient)
                    st.rerun()
                else:
                    st.error(f"Erro ao buscar produtos semelhantes: {response_similares.status_code}")
        else:
            st.error(f"Erro ao buscar produto: {response_produto.status_code}")
# --- Página Inicial / Lista de Produtos ---
if st.session_state.page == "home":
    st.write("Digite um produto acima e clique em Buscar para ver os resultados.")

elif st.session_state.page == "lista":
    st.subheader("Resultados da Busca")
    
    # Exibir produtos em cards
    for p in st.session_state.results:
        with st.container():
            st.markdown(f"""
                <div style='border:1px solid #ccc; padding:10px; border-radius:10px; margin-bottom:10px;'>
                    <h3 style='color:#FF69B4;'>{p['name']}</h3>
                    <p><b>Marca:</b> {p['brand']}</p>
                    <p><b>Preço:</b> {p['price']}<b> Reais</b></p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Ver {p['name']}", key=p['name']):
                st.session_state.current_product = p
                st.session_state.page = "produto"
                st.rerun()

    if st.button("Voltar"):
        st.session_state.page = "home"
        st.rerun()

# --- Página do Produto ---
elif st.session_state.page == "produto":
    produto = st.session_state.current_product
    if produto:
        st.markdown(f"""
        <div style='background-color:#FFF0F5; padding:15px; border-radius:15px;'>
            <h2>{produto['name']}</h2>
            <p><b>Marca:</b> {produto['brand']}</p>
            <p><b>Ingredientes:</b> {produto['ingredients']}</p>
            <p><b>Preço:</b> {produto['price']}<b> Reais</b></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("Produtos Semelhantes")

        # Buscar produtos semelhantes
        payload = {"ingredient": produto["name"]}
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            similares = response.json().get("results", [])
            similares = [s for s in similares if s["name"] != produto["name"]]

            for s in similares:
                with st.container():
                    st.markdown(f"""
                        <div style='border:1px solid #ccc; padding:10px; border-radius:10px; margin-bottom:10px;'>
                            <h4 style='color:#FF69B4;'>{s['name']}</h4>
                            <p><b>Marca:</b> {s['brand']}</p>
                            <p><b>Preço:</b> {s['price']}<b> Reais</b></p>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(s["name"], key=f"similar_{s['name']}"):
                        st.session_state.current_product = s
                        st.session_state.page = "produto"
                        st.rerun()

    if st.button("Voltar para lista"):
        st.session_state.page = "lista"
    st.rerun()