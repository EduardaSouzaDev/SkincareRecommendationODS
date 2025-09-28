import pandas as pd
import random as rd
import numpy as np
import sys

sys.stdout.reconfigure(encoding="utf-8")

df_users = pd.read_csv("backend/data/usersAvaliation.csv")
df_ingredients = pd.read_csv("backend/data/cosmetic.csv")

MAX = 6
MIN = 0
COS_MIN = 1
COS_MAX = 1472

def generate_new_ratings():
    rating = np.random.randint(low=MIN, high=MAX, size=len(df_users))
    df_users["rate"] = rating

def generate_number_of_avaliation():
    rand_num = rd.randint(MIN, 10)

def fill_csv():
    generate_new_ratings()
    cosmetic = []
    cosmetics_id = np.random.randint(low=COS_MIN, high=COS_MAX, size=(len(df_users)))
    
    for id in cosmetics_id:
        cosmetic.append(df_ingredients["name"][id])
    df_users["cosmetic"] = cosmetic
    #debug print(df_users)
    df_users.to_csv("backend/data/usersAvaliation.csv", index=False)

for i in range(COS_MIN, len(df_users)):
    df_users.loc[i, "id"] = i
    df_users.to_csv("backend/data/usersAvaliation.csv", index=False)

print(df_users)

#fill_csv()
