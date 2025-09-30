# accuracy_test.py
import pandas as pd
import numpy as np

# 1️⃣ Carrega o CSV
def load_user_data():
    return pd.read_csv("data/more_ava_simulated.csv")

df_users = load_user_data()
# Mantém apenas as colunas relevantes
df = df_users[['name', 'cosmetic', 'rate']]

# Função de recomendação colaborativa por usuário (Pearson)
def recommend_by_user(train_df, target_user, top_k_neighbors=3, top_n_products=5):
    rating_matrix = train_df.pivot_table(index='name', columns='cosmetic', values='rate', fill_value=0)
    if target_user not in rating_matrix.index:
        return []

    user_ratings = rating_matrix.loc[target_user]
    similarities = {}

    for other_user in rating_matrix.index:
        if other_user == target_user:
            continue
        other_ratings = rating_matrix.loc[other_user]
        common_mask = (user_ratings != 0) & (other_ratings != 0)
        if common_mask.sum() == 0:
            sim = 0
        else:
            sim = np.corrcoef(user_ratings[common_mask], other_ratings[common_mask])[0, 1]
            if np.isnan(sim):
                sim = 0
        similarities[other_user] = sim

    top_neighbors = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:top_k_neighbors]

    product_scores = {}
    for neighbor, sim in top_neighbors:
        neighbor_ratings = rating_matrix.loc[neighbor]
        for product, rating in neighbor_ratings.items():
            if user_ratings[product] == 0 and rating > 0:
                product_scores[product] = product_scores.get(product, 0) + sim * rating

    recommended = sorted(product_scores.items(), key=lambda x: x[1], reverse=True)[:top_n_products]
    return [p[0] for p in recommended]

# 2️⃣ Avaliação de acurácia, precisão e recall
results = []

for user in df['name'].unique():
    user_data = df[df['name'] == user]
    if len(user_data) < 2:
        continue  # pula usuários com menos de 2 avaliações

    # Divide treino/teste (50%-50%)
    user_data = user_data.sample(frac=1, random_state=42)  # embaralha
    split = len(user_data) // 2
    train_df = user_data.iloc[:split]
    test_df = user_data.iloc[split:]

    # Treino: todas as avaliações dos outros usuários + treino do usuário
    train_df_full = pd.concat([df[df['name'] != user], train_df], ignore_index=True)

    # Gera recomendações
    recommended = recommend_by_user(train_df_full, user, top_k_neighbors=3, top_n_products=5)

    # Itens relevantes no teste
    test_positive = test_df[test_df['rate'] >= 3]['cosmetic'].tolist()  # nota >=3
    hits = sum([1 for prod in recommended if prod in test_positive])

    total_recommended = len(recommended)
    total_relevant = len(test_positive)

    accuracy = hits / total_recommended if total_recommended > 0 else 0
    precision = hits / total_recommended if total_recommended > 0 else 0
    recall = hits / total_relevant if total_relevant > 0 else 0

    results.append({
        'user': user,
        'hits': hits,
        'recommended': total_recommended,
        'relevant': total_relevant,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall
    })

# Converte em DataFrame
df_results = pd.DataFrame(results)

# Exibe resultados
print(df_results)
print(f"\nAcurácia média: {df_results['accuracy'].mean():.2%}")
print(f"Precisão média: {df_results['precision'].mean():.2%}")
print(f"Recall médio: {df_results['recall'].mean():.2%}")
