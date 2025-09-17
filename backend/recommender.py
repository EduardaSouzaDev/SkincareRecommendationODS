import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv("backend/data/cosmetic.csv")

# Vetorizacao
vectorizer = CountVectorizer(binary=True, token_pattern=r'[^,]+')
X = vectorizer.fit_transform(data['ingredients'].fillna(""))

# Similaridade
similaridade = cosine_similarity(X)
similaridade = pd.DataFrame(similaridade, index=data['name'], columns=data['name'])

def recommend(nome_produto, top_n=5):

    if nome_produto not in similaridade.index:
        return "Produto não encontrado no dataset."

    # Ordena os produtos pelo grau de similaridade
    similares = similaridade[nome_produto].sort_values(ascending=False)

    # Remove o próprio produto e pega os top-N
    top_produtos = similares.drop(nome_produto).head(top_n)

    # Retornar informações básicas
    return data[data['name'].isin(top_produtos.index)][['name', 'brand', 'ingredients']]