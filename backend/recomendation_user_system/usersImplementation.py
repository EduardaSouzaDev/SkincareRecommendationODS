import pandas as pd
import random as rd
import numpy as np
import sys

sys.stdout.reconfigure(encoding="utf-8")

df_users = pd.read_csv("backend/data/usersAvaliation.csv")
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

def fill_csv():
    global df_avaliation
    
    avaliation = []
    
    for i in range(MIN, numberofusers+1):
        variant = np.random.randint(low = 1, high = 11, size = numberofusers)   
    
    for j in variant:
        position = rd.randint(0, numberofusers)
        for k in range(0, j):#faz repetir para cada uma das posições do CSV
            id = rd.randint(COS_MIN, COS_MAX-1)
            av = {"name" : df_users["name"][j], "cosmetic" : df_ingredients["name"][id], "rate" : rd.randint(COS_MIN, 5), "id" : position} #ok
            avaliation.append(av)
            print(avaliation)
            add_ava = pd.DataFrame(avaliation)
            df_avaliation = pd.concat([df_avaliation, add_ava], ignore_index=True)
        print(df_avaliation)
        df_avaliation = df_avaliation.drop_duplicates(inplace=False)
        df_avaliation.to_csv("backend/data/more_ava.csv", index=False)
        avaliation = []
        add_ava = add_ava[0:0]  
    

'''def update_id():
    for i in range(MIN, len(df_users)):
        df_users.loc[i, "id"] = i
        df_users.to_csv("backend/data/usersAvaliation.csv", index=False)'''

#print(df_users)

fill_csv()
