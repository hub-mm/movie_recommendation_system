# ./scripts/data_management/data_preprocess_credits.py
import pandas as pd


def preprocess_credits(filepath='./data/movies_dataset/7/credits.csv'):
    df = pd.read_csv(filepath, dtype='unicode')
    df['id'] = df['id'].astype('int')

    return df