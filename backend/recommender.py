import pandas as pd
import streamlit as st
from math import sqrt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv("backend/data/cosmetic.csv")
<<<<<<< HEAD


def load_user_data():
    return pd.read_csv("backend\data\more_ava.csv")

df_users = load_user_data()

=======
df_users = pd.read_csv("backend/data/more_ava.csv")
>>>>>>> parent of e130a4c (bring updates)

# Vetorizacao
vectorizer = CountVectorizer(binary=True, token_pattern=r'[^,]+')
X = vectorizer.fit_transform(data['ingredients'].fillna(""))

# Similaridade
similaridade = cosine_similarity(X)
similaridade = pd.DataFrame(similaridade, index=data['name'], columns=data['name'])

def recommend_by_ingredients(nome_produto, top_n=10):

    if nome_produto not in similaridade.index:
        return "Produto não encontrado no dataset."

    # Ordena os produtos pelo grau de similaridade
    similares = similaridade[nome_produto].sort_values(ascending=False)

    # Remove o próprio produto e pega os top-N
    top_produtos = similares.drop(nome_produto).head(top_n)

    # Retornar informações básicas
    produto_buscado = data[data['name'] == nome_produto][['name', 'brand', 'ingredients', 'price']]
    
    produtos_similares = data[data['name'].isin(top_produtos.index)][['name', 'brand', 'ingredients','price']]

    # Junta produto buscado + similares
    resultado_final = pd.concat([produto_buscado, produtos_similares], ignore_index=True)

    dolar_para_real = 5.3  

    # Converter e formatar
    resultado_final['price'] = resultado_final['price'].apply(
        lambda x: f"R$ {x * dolar_para_real:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

    return resultado_final

def filter_cosmetics(key_word):
    filter = df_users["cosmetic"].str.contains(key_word, case=False, na=False)
    return filter

def filter_user(key_word):
    filter = df_users["name"].str.contains(key_word, case=False, na=False)
    return filter

def manhattan(rating1, rating2):
    
    distance = 0
    commonRatings = False  # Flag para saber se os dois usuários têm músicas em comum

    for key in rating1:
        if key in rating2:
            distance += abs(rating1[key] - rating2[key])  # Soma a diferença absoluta das notas
            commonRatings = True

    if commonRatings:
        return distance  # Retorna a distância total
    else:
        return -1  # Retorna -1 se não houver músicas em comum

def computeNearestNeighbor(username):
    distances = []  # Lista de tuplas (distância, nome_do_usuário)


    for user in df_users:
        if user != username:
            distance = manhattan(users[user], users[username])  # Calcula a distância
            distances.append((distance, user))

    distances.sort()  # Ordena pela menor distância (mais semelhante primeiro)
    return distances

def recommend(username, users):
    # Chama a função anterior para encontrar o usuário mais próximo e pega apenas o nome desse usuário.
    nearest = computeNearestNeighbor(username, users)#[0][1]  # Nome do usuário mais próximo
    recommendations = []  # Lista de recomendações

    # Armazena as avaliações do vizinho mais próximo e do usuário atual em variáveis separadas
    neighborRatings = users[nearest]  # Avaliações do vizinho
    userRatings = users[username]  # Avaliações do usuário

    # Para cada item avaliado pelo vizinho, verifica se o usuário ainda não avaliou.
    # Se for o caso, adiciona esse item à lista de recomendações.
    for artist in neighborRatings:
        if artist not in userRatings:
            recommendations.append((artist, neighborRatings[artist]))  # Adiciona recomendação

    # Ordena por maior pontuação do vizinho
    return sorted(recommendations, key=lambda artistTuple: artistTuple[1], reverse=True)

# Função que monta a interface do aplicativo no Streamlit
def recommend_app():
    st.title("Sistema de Recomendação Colaborativo de Cosméticos")  # Título do app

    username = st.text_input("Digite o nome de usuário:")  # Campo de entrada para o nome
    #splitted_username = re.split("[.-,/\' %]", username)
    #print(splitted_username)
    if st.button("Recomendar produtos"):  # Botão para gerar recomendação
        if username in users:
            recommendations = recommend(username, users)  # Gera recomendações
            st.write(f"Recomendações para {username}:")
            for recommendation in recommendations:
                st.write(f"{recommendation[0]} - Pontuação: {recommendation[1]}")  # Exibe recomendações
        else:
            st.write("Nome de usuário não encontrado. Por favor, insira um nome de usuário válido.")  # Mensagem de erro
