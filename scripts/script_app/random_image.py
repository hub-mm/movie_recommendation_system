# ./scripts/script_app/random_image.py
import pickle
import random


def random_img(n=24):
    data_path = './data/user_built/'
    with open(f"{data_path}/preprocessed_df_movies.pkl", 'rb') as f:
        df = pickle.load(f)

    base_url = 'https://image.tmdb.org/t/p/w500'
    movies = []
    while len(movies) < n:
        num = random.randint(0, len(df) - 1)
        title = df['title'].iloc[num]
        full_url = base_url + str(df['poster_path'].iloc[num])

        if title in movies:
            num = random.randint(0, len(df) - 1)
            title = df['title'].iloc[num]
            full_url = base_url + str(df['poster_path'].iloc[num])

        movies.append({'title': title, 'full_url': full_url})

    return movies