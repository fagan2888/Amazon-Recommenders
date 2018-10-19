import pandas as pd
import numpy as np
import sqlite3 as sq
from math import sqrt

path = 'C:/users/arjun/Desktop/amazon.db'

#TO-DO: SHOULD I ONLY DO THIS WITH USERS WITH OVER A CERTAIN AMOUNT OF RATINGS?

def import_data(db_path):
    conn = sq.connect(db_path) #sqliteDB path goes in parantheses
    crsr = conn.cursor()

    df = pd.read_sql_query('''
                SELECT DISTINCT
                    customer_id,
                    product_id,
                    star_rating
                FROM amazon_music_reviews
                WHERE LENGTH(STAR_RATING) < 2
                AND product_id = 'B00Q9KEZV0' LIMIT 10000''', conn)

    df['star_rating'] = df['star_rating'].astype(float)
    df['star_rating'] = df['star_rating'].astype(int) #convert rating to integer type

    return df

#df = import_data(path)


def euclidean_similarity(user1, user2, data):
    #instead of storing data in both_rated why not just use counter, if it is just a flag for
    both_rated = {}

    u1_data = data.loc[data['customer_id']==user1]
    u2_data = data.loc[data['customer_id']==user2]

    for item in u1_data['product_id']:
        if item in u2_data['product_id'].unique():
            both_rated[item]=1

    if len(both_rated)==0:  #work this into distance formula to account for volume
        return 0

    euclidean_distance = []

    for item in u1_data['product_id']:
        if item in u2_data['product_id'].unique():
            u1_avg_rating = np.mean(u1_data['star_rating'].loc[u1_data['product_id']==item].tolist())
            u2_avg_rating = np.mean(u2_data['star_rating'].loc[u2_data['product_id']==item].tolist())

            euclidean_distance.append((u1_avg_rating - u2_avg_rating)**2)

    sum_of_euclidean_distance = sum(euclidean_distance)

    inverted_euclidean_distance = 1/(1+sqrt(sum_of_euclidean_distance))

    return user1, user2, inverted_euclidean_distance

'''
for a in df['customer_id']:
    for b in df['customer_id']:
        print(euclidean_similarity(a, b, df))
'''

#pearson correlation function -- still working on this
def pearson_similarity(user1, user2, data):
    #instead of storing data in both_rated why not just use counter, if it is just a flag for
    both_rated = {}

    u1_data = data.loc[data['customer_id']==user1]
    u2_data = data.loc[data['customer_id']==user2]

    for item in u1_data['product_id']:
        if item in u2_data['product_id'].unique():
            both_rated[item]=1

    if len(both_rated)==0:
        return 0

    '''add up all preferences of each user'''
    u1_pref_sum = sum(u1_data['star_rating'].tolist())
    u2_pref_sum = sum(u2_data['star_rating'].tolist())

    '''sum up the squares of preferences of each user'''
    u1_square_pref_sum = sum((u1_data['star_rating'].tolist() ** 2))
    u2_square_pref_sum = sum((u2_data['star_rating'].tolist() ** 2))