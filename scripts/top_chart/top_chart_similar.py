# ./scripts/top_chart/top_chart_similar.py
from scripts.data_management.data_merge_similar import preprocess_df
import os
import pickle
import pandas as pd
import numpy as np


def get_directors(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

def build_similar_chart(title='batman', amount=30):
    title = title.lower()

    data_path = './data/user_built/'
    if not os.path.exists(data_path):
        preprocess_df()

    with open(f"{data_path}/preprocessed_df.pkl", 'rb') as f:
        df = pickle.load(f)

    with open(f"{data_path}/cosine_sim.pkl", 'rb') as f:
        cosine_sim = pickle.load(f)

    with open(f"{data_path}/indices.pkl", 'rb') as f:
        indices = pickle.load(f)

    if title not in indices:
        print(f"Title '{title}' not found!")
        return pd.DataFrame()

    val = indices[title]
    if isinstance(val, pd.Series):
        idx = val.iloc[0]
    else:
        idx = val

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:amount + 1]

    movie_indices = [i[0] for i in sim_scores]
    cols_to_show = ['title', 'release_date', 'vote_count', 'vote_average', 'popularity', 'genres', 'cast']
    df['title'] = df['title'].fillna('').str.title()

    return df.iloc[movie_indices][cols_to_show]