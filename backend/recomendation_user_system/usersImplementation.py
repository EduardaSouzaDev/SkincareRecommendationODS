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
    cosmetic = []
    cosmetics_id = np.random.randint(low=COS_MIN, high=COS_MAX, size=(len(df_users)))
    
    for i in range(MIN, len(df_users["id"])+1):
        variant = np.random.randint(low = 1, high = 11, size = 18)   
    
    for j in variant:
        position = rd.randint(0, 18)
        for k in range(0, j):#faz repetir para cada uma das posições do CSV
            id = rd.randint(COS_MIN, COS_MAX)
            avaliation = {"id" : [position], "name" : [df_ingredients["name"][id]], "rate" : [rd.randint(COS_MIN, MAX)]} #ok
            #for id in cosmetics_id:
                #cosmetic.append(df_ingredients["name"][id]) #cria uma lista de cosmeticos
            #df_users.iloc[j, "cosmetic"] = cosmetic
            #df_users["cosmetic"] = df_ingredients["name"][id]
            #print(df_users["name"][j])
            #print(f"product: {avaliation}") - ok
            add_ava = pd.DataFrame(avaliation)
        print(f"{add_ava}")
        avaliation = {}
        #df_users["cosmetic"] = cosmetic
        #cosmetic = []
    #print(df_users)
    generate_new_ratings()
    #df_users.to_csv("backend/data/usersAvaliation.csv", index=False)     
    

'''def update_id():
    for i in range(MIN, len(df_users)):
        df_users.loc[i, "id"] = i
        df_users.to_csv("backend/data/usersAvaliation.csv", index=False)'''

#print(df_users)

fill_csv()
