# ./scripts/data_management/data_preprocess_ratings.py
import pandas as pd


def preprocess_ratings(filepath='./data/movies_dataset/7/ratings.csv'):
    df = pd.read_csv(filepath, dtype='unicode')
    df['userId'] = df['userId'].astype('int')
    df['movieId'] = df['movieId'].astype('int')
    df['rating'] = df['rating'].astype('float')

    return df