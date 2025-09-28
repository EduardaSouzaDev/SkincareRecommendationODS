import pandas as pd
import random as rd
import time
import numpy as np
import sys


sys.stdout.reconfigure(encoding="utf-8")
rd.seed(time.time_ns())

df_users = pd.read_csv("backend/data/usersAvaliation.csv")
df_ingredients = pd.read_csv("backend/data/cosmetic.csv", encoding="utf-8")

MAX = 6
MIN = 0
COS_MIN = 1
COS_MAX = 1472
ID = df_ingredients["id"]

def generate_new_ratings():
    rating = np.random.randint(low=MIN, high=MAX, size=len(df_users))
    df_users["rate"] = rating
    #df_users.to_csv("usersAvaliation.csv", index=False)

def generate_cosmetics():
    id = np.random.randint(low=COS_MIN, high=COS_MAX, size=(len(df_users)))
    return id

def fill_csv():
    generate_new_ratings()
    cosmetic = []
    cosmetics_id = np.random.randint(low=COS_MIN, high=COS_MAX, size=(len(df_users)))
    for id in cosmetics_id:
        cosmetic.append(df_ingredients["name"][id])
    df_users["cosmetic"] = cosmetic
    print(df_users)
    df_users.to_csv("backend/data/usersAvaliation.csv", index=False)



#generate_new_ratings()
fill_csv()
#print(chr(8482))
#print(df_users)

#print(rand_number)


#rand_number_generator = rand.uniform(3.0, 5.0)
#rand_float = round(rand_number_generator, 1)




