import pandas as pd
import random as rd
import numpy as np
import sys

sys.stdout.reconfigure(encoding="utf-8")

df_users = pd.read_csv("data/usersAvaliation.csv")
df_ingredients = pd.read_csv("backend/data/cosmetic.csv")
df_avaliation = pd.read_csv("backend/data/more_ava.csv")

MAX = 6
MIN = 0
COS_MIN = 1
COS_MAX = 1472
numberofusers = 18


def generate_new_ratings():
    rating = np.random.randint(low=MIN, high=MAX, size= numberofusers)
    df_users["rate"] = rating

def generate_number_of_avaliation():
    rand_num = rd.randint(MIN, 10)

def fill_csv(number_of_users, min_rate=1, max_rate=5):
    global df_avaliation

    new_aval = []

    for user_idx in range(number_of_users):
        # Quantas avaliações esse usuário vai fazer (aleatório, entre 1 e 10)
        num_ratings = np.random.randint(1, 11)
        
        for _ in range(num_ratings):
            # Escolhe produto aleatório
            product_idx = np.random.randint(0, len(df_ingredients))
            av = {
                "name": df_users["name"].iloc[user_idx],
                "cosmetic": df_ingredients["name"].iloc[product_idx],
                "rate": np.random.randint(min_rate, max_rate+1),
                "id": user_idx
            }
            new_aval.append(av)

    # Adiciona ao dataframe existente e remove duplicados
    df_new = pd.DataFrame(new_aval)
    df_avaliation = pd.concat([df_avaliation, df_new], ignore_index=True)
    df_avaliation.drop_duplicates(inplace=True)

    # Salva no CSV
    df_avaliation.to_csv("backend/data/more_ava.csv", index=False)
    print(f"{len(new_aval)} avaliações adicionadas com sucesso!")


'''def update_id():
    for i in range(MIN, len(df_users)):
        df_users.loc[i, "id"] = i
        df_users.to_csv("backend/data/usersAvaliation.csv", index=False)'''

def filter_items(key_word):

    filter = df_avaliation["cosmetic"].str.contains(key_word, case=False, na=False)
    #print(df_avaliation[filtro])
    return filter
fill_csv(18)
