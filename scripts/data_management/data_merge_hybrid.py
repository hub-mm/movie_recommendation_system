# ./scripts/data_management/data_merge_hybrid.py
from scripts.data_management.data_preprocess_links import preprocess_links
from scripts.data_management.data_merge_similar import preprocess_df
import os
import pickle


def merge_df():
    df_id_map = preprocess_links()

    data_path = './data/user_built/'
    if not os.path.exists(data_path):
        preprocess_df()

    data_path = './data/user_built/'
    with open(f"{data_path}/preprocessed_df.pkl", 'rb') as f:
        df = pickle.load(f)

    df_id_map = df_id_map.merge(df[['title', 'id']], on='id').set_index('title')

    return df_id_map