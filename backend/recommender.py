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