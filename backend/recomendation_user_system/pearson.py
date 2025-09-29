import streamlit as st
import pandas as pd
from math import sqrt

# Função para carregar o dataset CSV
def load_data():
    try:
        # Carregar o arquivo CSV e verificar se as colunas estão presentes
        data = pd.read_csv('dataset.csv')
        if 'Username' not in data.columns or 'Game' not in data.columns or 'Rating' not in data.columns:
            st.error("O arquivo CSV deve conter as colunas: 'Username', 'Game', e 'Rating'.")
            return pd.DataFrame(columns=["Username", "Game", "Rating"])
        return data
    except FileNotFoundError:
        st.warning("Arquivo CSV não encontrado. Criando um novo arquivo.")
        return pd.DataFrame(columns=["Username", "Game", "Rating"])

# Função para salvar o dataset atualizado no CSV
def save_data(data):
    data.to_csv('dataset.csv', index=False)

# Função para calcular a similaridade de Pearson
def pearson(rating1, rating2):
    sum_xy = 0
    sum_x = 0
    sum_y = 0
    sum_x2 = 0
    sum_y2 = 0
    n = 0
    for key in rating1:
        if key in rating2:
            n += 1
            x = rating1[key]
            y = rating2[key]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += pow(x, 2)
            sum_y2 += pow(y, 2)
    denominator = sqrt(sum_x2 - pow(sum_x, 2) / n) * sqrt(sum_y2 - pow(sum_y, 2) / n)
    if denominator == 0:
        return 0
    else:
        return (sum_xy - (sum_x * sum_y) / n) / denominator

# Função para calcular os vizinhos mais próximos
def computeNearestNeighbor(username, users_ratings):
    distances = []
    current_user_ratings = users_ratings[users_ratings['Username'] == username].set_index('Game')['Rating'].to_dict()

    for user in users_ratings['Username'].unique():
        if user != username:
            other_user_ratings = users_ratings[users_ratings['Username'] == user].set_index('Game')['Rating'].to_dict()
            distance = pearson(current_user_ratings, other_user_ratings)
            distances.append((distance, user))

    distances.sort(reverse=True)
    return distances

# Função para recomendar jogos
def recommend(username, users_ratings):
    neighbors = computeNearestNeighbor(username, users_ratings)
    if not neighbors:
        st.write(f"Nenhum vizinho encontrado para o usuário {username}.")
        return []

    nearest = neighbors[0][1]
    st.write(f"Vizinho mais próximo encontrado: {nearest}")

    neighbor_ratings = users_ratings[users_ratings['Username'] == nearest].set_index('Game')['Rating'].to_dict()
    user_ratings = users_ratings[users_ratings['Username'] == username].set_index('Game')['Rating'].to_dict()

    recommendations = []
    for game in neighbor_ratings:
        if game not in user_ratings:
            recommendations.append((game, neighbor_ratings[game]))

    if not recommendations:
        st.write("Nenhuma recomendação encontrada.")
    
    return sorted(recommendations, key=lambda x: x[1], reverse=True)

# Função para criar o aplicativo Streamlit
def recommend_app():
    st.title("Sistema de Recomendação Colaborativo de Jogos")
    
    # Carregar o dataset CSV
    users_ratings = load_data()
    
    # Exibir os usuários existentes
    if not users_ratings.empty:
        username = st.selectbox("Selecione o nome de usuário:", users_ratings['Username'].unique())
    
        # Selecionar um jogo e avaliar
        game_to_rate = st.selectbox("Selecione um jogo para avaliar:", users_ratings['Game'].unique())
        rating = st.slider("Avaliação (1-5):", 1, 5)
    
        if st.button("Avaliar Jogo"):
            new_rating = pd.DataFrame({'Username': [username], 'Game': [game_to_rate], 'Rating': [rating]})
            users_ratings = pd.concat([users_ratings, new_rating], ignore_index=True)
            save_data(users_ratings)
            st.write(f"Avaliação para {game_to_rate} adicionada com sucesso!")
    
        if st.button("Recomendar Jogos"):
            st.write(f"Gerando recomendações para {username}...")
            recommendations = recommend(username, users_ratings)
            
            if recommendations:
                st.write(f"Recomendações para {username}:")
                for recommendation in recommendations:
                    st.write(f"{recommendation[0]} - Pontuação: {recommendation[1]}")
            else:
                st.write(f"Nenhuma recomendação disponível para {username}.")
    
    # Adicionar um novo usuário
    new_user = st.text_input("Digite o nome de um novo usuário:")
  
    if st.button("Adicionar Novo Usuário"):
        if new_user not in users_ratings['Username'].unique():
            users_ratings = pd.concat([users_ratings, pd.DataFrame({'Username': [new_user], 'Game': [""], 'Rating': [""]})], ignore_index=True)
            save_data(users_ratings)
            st.write(f"Novo usuário {new_user} adicionado com sucesso! Recarregue a página para vê o novo usuário na lista")           
        else:
            st.write(f"O usuário {new_user} já existe!")

def main():
    recommend_app()

if __name__ == "__main__":
    main()  