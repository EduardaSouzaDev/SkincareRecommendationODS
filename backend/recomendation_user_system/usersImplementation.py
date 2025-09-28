import pandas as pd
import random as rd
import time
import numpy as np

rd.seed(time.time_ns())

df_users = pd.read_csv("backend/data/usersAvaliation.csv")
df_ingredients = pd.read_csv("backend/data/cosmetic.csv")

MAX = 6
MIN = 0
COS_MIN = 1
COS_MAX = 1472
ID = df_ingredients["id"]

def generate_new_ratings():
    rating = np.random.randint(low=MIN, high=MAX, size=len(df_users))
    df_users["rate"] = rating
    df_users.to_csv("backend/data/usersAvaliation.csv", index=False)


def generate_cosmetics():
    
    return id


#generate_new_ratings()

print(df_users)

#print(rand_number)


#rand_number_generator = rand.uniform(3.0, 5.0)
#rand_float = round(rand_number_generator, 1)




