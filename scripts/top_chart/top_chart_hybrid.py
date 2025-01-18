# ./scripts/top_chart/top_chart_hybrid.py
from scripts.data_management.data_merge_hybrid import merge_df
from scripts.build_model.build_model_collab_filtering import build_model_filtering
import os
import pickle
import pandas as pd


def build_chart_hybrid(user_id=1, title='batman', amount=30):
    df_id_map = merge_df()

    data_path = './data/user_built/'
    with open(f"{data_path}/preprocessed_df.pkl", 'rb') as f:
        df = pickle.load(f)

    with open(f"{data_path}/cosine_sim.pkl", 'rb') as f:
        cosine_sim = pickle.load(f)

    with open(f"{data_path}/indices.pkl", 'rb') as f:
        indices = pickle.load(f)

    model_path = './model/'
    if not os.path.exists(model_path):
        build_model_filtering()

    with open(f"{model_path}/model_filtering.pkl", 'rb') as f:
        svd = pickle.load(f)

    indices_map = df_id_map.set_index('id')

    if title not in indices:
        print(f"Title '{title}' not found!")
        return pd.DataFrame()

    val = indices[title]
    if isinstance(val, pd.Series):
        idx = val.iloc[0]
    else:
        idx = val

    sim_scores = list(enumerate(cosine_sim[int(idx)]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:amount + 1]

    movie_indices = [i[0] for i in sim_scores]
    df = df.iloc[movie_indices][
        ['title', 'release_date', 'vote_count', 'vote_average', 'popularity', 'genres', 'cast', 'id', 'poster_path']
    ]
    df['est'] = df['id'].apply(lambda x: svd.predict(user_id, int(indices_map.loc[x]['moviesId']), r_ui=None).est)

    df['title'] = df['title'].fillna('').str.title()
    movies = df.sort_values('est', ascending=False)

    base_url = 'https://image.tmdb.org/t/p/w500'
    movies['poster_path'] = base_url + movies['poster_path'].astype(str)

    movies = movies.head(amount).to_dict(orient='records')

    return movies