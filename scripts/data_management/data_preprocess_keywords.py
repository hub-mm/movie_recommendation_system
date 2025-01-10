# ./scripts/data_management/data_preprocess_keywords.py
import pandas as pd


def preprocess_keywords(filepath='./data/movies_dataset/7/keywords.csv'):
    df = pd.read_csv(filepath, dtype='unicode')
    df['id'] = df['id'].astype('int')

    return df