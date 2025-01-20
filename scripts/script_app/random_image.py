# ./scripts/script_app/random_image.py
import pickle
import random
import ast


def random_img(amount=20):
    data_path = './data/user_built/'
    with open(f"{data_path}/preprocessed_df_movies.pkl", 'rb') as f:
        df = pickle.load(f)

    base_url = 'https://image.tmdb.org/t/p/w500'
    movies = []
    while len(movies) < amount:
        num = random.randint(0, len(df) - 1)
        title = df['title'].iloc[num]
        full_url = base_url + str(df['poster_path'].iloc[num])
        release_date = df['release_date'].iloc[num]
        original_language = df['original_language'].iloc[num]
        genres = df['genres'].iloc[num]
        genres_list = ast.literal_eval(genres)
        genres_string = ', '.join([genre['name'] for genre in genres_list])
        vote_average = df['vote_average'].iloc[num]
        production_companies = df['production_companies'].iloc[num]
        production_companies_list = ast.literal_eval(production_companies)
        production_companies_string = ', '.join([production['name'] for production in production_companies_list])

        if title in movies:
            num = random.randint(0, len(df) - 1)
            title = df['title'].iloc[num]
            full_url = base_url + str(df['poster_path'].iloc[num])

        movies.append({
            'title': title,
            'full_url': full_url,
            'release_date': release_date,
            'original_language': original_language,
            'genres': genres_string,
            'vote_average': vote_average,
            'production_comp': production_companies_string
        })

    return movies