import pandas as pd
import random

# Usuários e produtos
users = ["Fatima", "Vitoria", "Alex", "Bia", "Nazare", "Sheila"]
products = [
    "Crème de la Mer", "Facial Treatment Essence", "Protini™ Polypeptide Cream",
    "The Moisturizing Soft Cream", "Your Skin But Better™ CC+™ Cream with SPF 50+",
    "The Water Cream", "Lala Retro™ Whipped Cream", "Virgin Marula Luxury Facial Oil",
    "Ultra Facial Cream"
]

# Gerar avaliações
data = []
for user in users:
    for product in products:
        # Decide aleatoriamente se o usuário avaliou este produto
        avaliou = random.random() < 0.7  # 70% de chance de ter avaliação
        if avaliou:
            rate = random.choice([3, 4, 5])
        else:
            rate = 0
        data.append({"name": user, "cosmetic": product, "rate": rate})

# Criar DataFrame
df = pd.DataFrame(data)

# Salvar CSV
df.to_csv("more_ava_simulated.csv", index=False)
print(df)
