import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("backend/data/cosmetic.csv")

# Vetorizacao
vectorizer = CountVectorizer(binary=True, token_pattern=r'[^,]+')
X = vectorizer.fit_transform(df['ingredients'].fillna(""))

# Similaridade
similaridade = cosine_similarity(X)
similaridade = pd.DataFrame(similaridade, index=df['name'], columns=df['name'])

def recommend(nome_produto, top_n=5):
    if nome_produto not in similaridade.index:
        return []

    similares = similaridade[nome_produto].sort_values(ascending=False)
    top_produtos = similares.drop(nome_produto).head(top_n)

    return df[df['name'].isin(top_produtos.index)][['name', 'brand', 'ingredients']].to_dict(orient="records")
