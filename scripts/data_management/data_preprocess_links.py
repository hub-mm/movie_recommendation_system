# ./scripts/data_management/data_preprocess_links.py
import numpy as np
import pandas as pd


def convert_int(x):
    try:
        return int(x)
    except ValueError:
        return np.nan

def preprocess_links(filepath='./data/movies_dataset/7/links.csv'):
    df = pd.read_csv(filepath, dtype='unicode')[['movieId', 'tmdbId']]
    df['tmdbId'] = df['tmdbId'].apply(convert_int)
    df.columns = ['moviesId', 'id']
    df['moviesId'] = df['moviesId'].astype(int)

    return df