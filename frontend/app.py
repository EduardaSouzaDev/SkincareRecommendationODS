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
if "usuario_digitado" not in st.session_state:
    st.session_state.usuario_digitado = ""
if "usuario_confirmado" not in st.session_state:
    st.session_state.usuario_confirmado = ""

# --- Container fixo no topo (título + busca) ---
with st.sidebar:
    st.header("Usuário")
    st.session_state.usuario_digitado = st.text_input(
        "Digite seu nome:", value=st.session_state.usuario_digitado
    )

    # Botão de confirmar
    if st.button("Confirmar"):
        if st.session_state.usuario_digitado.strip() != "":
            # Salva o valor confirmado
            st.session_state.usuario_confirmado = st.session_state.usuario_digitado.strip()
            st.success(f"Bem-vindo(a), {st.session_state.usuario_confirmado}!")
        else:
            st.warning("Por favor, digite um nome antes de confirmar.")

header_container = st.container()
with header_container:
    st.markdown("<h1 style='text-align:center; color:#FF69B4;'>💆🏻‍♀ Sistema de Recomendação Skincare 🫧</h1>", unsafe_allow_html=True)
    ingredient_input = st.text_input("Digite o produto:", value = None)
    if st.button("Buscar"):
        if st.session_state.usuario_confirmado == "":
            st.warning("Você precisa digitar seu nome na barra lateral antes de buscar.")
        else:
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
        # Card do produto
        st.markdown(f"""
        <div style='background-color:#FFF0F5; padding:15px; border-radius:15px;'>
            <h2>{produto['name']}</h2>
            <p><b>Marca:</b> {produto['brand']}</p>
            <p><b>Ingredientes:</b> {produto['ingredients']}</p>
            <p><b>Preço:</b> {produto['price']}<b> Reais</b></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)

        # --- Avaliação ---
        st.write("Avalie este produto:")
        st.markdown("---")
        rating = st.radio(
            "Escolha uma nota:",
            [1, 2, 3, 4, 5],
            horizontal=True,
            key=f"rating_{produto['name']}"
        )

        st.write(f"⭐ Você avaliou com {rating} estrela(s).")

        if st.button("Enviar Avaliação", key=f"avaliar_{produto['name']}"):
            if not st.session_state.usuario_confirmado:
                st.warning("Você precisa digitar e confirmar seu nome na barra lateral antes de avaliar.")
            else:
                payload = {
                    "usuario": st.session_state.usuario_confirmado,
                    "produto": produto["name"],
                    "avaliacao": rating
                }
                try:
                    response = requests.post("http://127.0.0.1:8000/avaliar", json=payload, timeout=10)
                    if response.status_code == 200:
                        st.success("Avaliação registrada com sucesso! ✅")

                        # Atualiza recomendações imediatamente
                        payload_user = {"username": st.session_state.usuario_confirmado}
                        response_user = requests.post("http://127.0.0.1:8000/recommend_user", json=payload_user)
                        if response_user.status_code == 200:
                            st.session_state.recomendados = response_user.json().get("results", [])
                        else:
                            st.error("Erro ao atualizar recomendações")
                    else:
                        st.error(f"Erro ao enviar avaliação: {response.status_code}")
                except Exception as e:
                    st.error(f"Erro na requisição: {e}")

        # --- Layout com produtos semelhantes e recomendados ---
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Produtos Semelhantes")
            payload_similares = {"ingredient": produto["name"]}
            response_similares = requests.post(API_URL, json=payload_similares)
            if response_similares.status_code == 200:
                similares = response_similares.json().get("results", [])
                similares = [s for s in similares if s["name"] != produto["name"]]

                for s in similares:
                    st.markdown(f"""
                        <div style='border:1px solid #ccc; padding:10px; border-radius:10px; margin-bottom:10px;'>
                            <h4 style='color:#FF69B4;'>{s['name']}</h4>
                            <p><b>Marca:</b> {s['brand']}</p>
                            <p><b>Preço:</b> {s['price']}<b> Reais</b></p>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Ver {s['name']}", key=f"similar_{s['name']}"):
                        st.session_state.current_product = s
                        st.session_state.page = "produto"
                        st.rerun()

        with col2:
            st.subheader("Recomendados para Você")
            recomendados = st.session_state.get("recomendados", [])
            if not recomendados:
                st.write("Nenhuma recomendação disponível.")
            else:
                for r in recomendados:
                    # pular se for o produto atual (não mostrar em recomendados)
                    if st.session_state.current_product and r["name"] == st.session_state.current_product["name"]:
                        continue  

                    st.markdown(f"""
                        <div style='border:1px solid #ccc; padding:10px; border-radius:10px; margin-bottom:10px;'>
                            <h4 style='color:#FF69B4;'>{r['name']}</h4>
                            <p><b>Marca:</b> {r['brand']}</p>
                            <p><b>Preço:</b> {r['price']} Reais</p>
                            <p><b>Score:</b> {r['score']:.2f}</p>
                        </div>
                    """, unsafe_allow_html=True)

                    if st.button(f"Ver {r['name']}", key=f"recomendado_{r['name']}"):
                        st.session_state.current_product = r
                        st.session_state.page = "produto"
                        st.rerun()

                    

    # Botão para voltar à lista
    if st.button("Voltar para lista"):
        st.session_state.page = "lista"
        st.rerun()
