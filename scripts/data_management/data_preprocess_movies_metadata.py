# ./scripts/data_management/data_preprocess_movies_metadata.py
from ast import literal_eval
import pandas as pd


def preprocess_movies_md(filepath='./data/movies_dataset/7/movies_metadata.csv'):
    df = pd.read_csv(filepath, dtype='unicode')
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce').apply(lambda x: x.date())
    df['genres'] = df['genres'].fillna('[]').apply(literal_eval).apply(
        lambda x: [i['name'] for i in x] if isinstance(x, list) else []
    )

    return df