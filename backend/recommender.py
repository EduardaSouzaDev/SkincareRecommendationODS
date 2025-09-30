import pandas as pd
import numpy as np
import streamlit as st
from math import sqrt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv("backend/data/cosmetic.csv")


def load_user_data():
    return pd.read_csv("backend\data\more_ava.csv")

df_users = load_user_data()


# Vetorizacao
vectorizer = CountVectorizer(binary=True, token_pattern=r'[^,]+')
X = vectorizer.fit_transform(data['ingredients'].fillna(""))

# Similaridade
similaridade = cosine_similarity(X)
similaridade = pd.DataFrame(similaridade, index=data['name'], columns=data['name'])

def recommend_by_ingredients(nome_produto, top_n=3):

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

from scipy.stats import pearsonr
import numpy as np

def recommend_by_user(username, top_k_neighbors=3, top_n_products=5):
    """
    Retorna lista de dicionários:
    [{ "name","brand","ingredients","price","score" }, ...]
    usando **similaridade de Pearson** entre usuários.
    """
    if username not in df_users['name'].values:
        return f"Usuário '{username}' não encontrado."

    # matriz usuário x produto (0 = sem avaliação)
    rating_matrix = df_users.pivot_table(index='name', columns='cosmetic', values='rate', fill_value=0)
    if username not in rating_matrix.index:
        return f"Usuário '{username}' não possui avaliações."

    user_ratings = rating_matrix.loc[username].values.reshape(1, -1)
    all_users = rating_matrix.index.tolist()

    # calcula similaridade Pearson com todos os outros usuários
    similarities = {}
    for other in all_users:
        if other != username:
            u = rating_matrix.loc[username].values
            v = rating_matrix.loc[other].values
            sim, _ = pearsonr(u, v)
            similarities[other] = 0 if np.isnan(sim) else sim

    # top K vizinhos
    top_neighbors = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:top_k_neighbors]

    # previsão ponderada para produtos que o usuário ainda não avaliou
    product_scores = {}
    cols = rating_matrix.columns
    for neighbor, sim in top_neighbors:
        neighbor_ratings = rating_matrix.loc[neighbor]
        for product, rating in neighbor_ratings.items():
            if user_ratings[0][cols.get_loc(product)] == 0 and rating > 0:
                weight = max(sim, 0.01)  # padding mínimo
                product_scores[product] = product_scores.get(product, 0) + weight * rating

    if not product_scores:
        return []

    # pega top N produtos
    recommended = sorted(product_scores.items(), key=lambda x: x[1], reverse=True)[:top_n_products]

    # monta resultado completo
    recommended_full = []
    dolar_para_real = 5.3
    for prod_name, score in recommended:
        row = data[data['name'] == prod_name]
        if not row.empty:
            row0 = row.iloc[0]
            price_raw = row0.get('price', None)
            if pd.notna(price_raw):
                try:
                    price_value = float(price_raw)
                    price_str = f"R$ {price_value * dolar_para_real:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                except Exception:
                    price_str = str(price_raw)
            else:
                price_str = "N/A"

            recommended_full.append({
                "name": row0.get('name', prod_name),
                "brand": row0.get('brand', 'Desconhecida'),
                "ingredients": row0.get('ingredients', ''),
                "price": price_str,
                "score": float(score)
            })
        else:
            recommended_full.append({
                "name": prod_name,
                "brand": "Desconhecida",
                "ingredients": "",
                "price": "N/A",
                "score": float(score)
            })

    return recommended_full

