# ./scripts/data_management/data_merge_similar.py
from scripts.data_management.data_preprocess_movies_metadata import preprocess_movies_md
from scripts.data_management.data_preprocess_credits import preprocess_credits
from scripts.data_management.data_preprocess_keywords import preprocess_keywords
import pandas as pd
import numpy as np
from ast import literal_eval
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import pickle


def get_directors(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

def preprocess_df():
    df = preprocess_movies_md()

    vote_counts = df[df['vote_count'].notnull()]['vote_count'].astype('float')
    min_votes = vote_counts.quantile(0.60)

    df = df[
        (df['vote_count'].astype('float') >= min_votes) & (df['vote_count'].notnull()) & (df['vote_average'].notnull())
        ][
        ['title', 'release_date', 'vote_count', 'vote_average', 'popularity', 'genres', 'tagline', 'overview', 'id', 'poster_path']
    ]

    df['title'] = df['title'].fillna('').str.lower()

    df['id'] = pd.to_numeric(df['id'], errors='coerce')
    df = df.dropna(subset=['id'])
    df['id'] = df['id'].astype(int)
    df_credits = preprocess_credits()
    df_keywords = preprocess_keywords()

    df = df.merge(df_credits, on='id')
    df = df.merge(df_keywords, on='id')

    df['cast'] = df['cast'].apply(literal_eval)
    df['crew'] = df['crew'].apply(literal_eval)
    df['keywords'] = df['keywords'].apply(literal_eval)
    df['cast_size'] = df['cast'].apply(lambda x: len(x))
    df['crew-size'] = df['crew'].apply(lambda x: len(x))

    df['director'] = df['crew'].apply(get_directors)
    df['cast'] = df['cast'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    df['cast'] = df['cast'].apply(lambda x: x[:3] if len(x) >= 3 else x)
    df['keywords'] = df['keywords'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    df['cast'] = df['cast'].apply(lambda x: [str.lower(i.replace(' ', ' ')) for i in x])

    df['director'] = df['director'].astype('str').apply(lambda x: str.lower(x.replace(' ', '')))
    df['director'] = df['director'].apply(lambda x: [x, x, x])

    s = df.apply(lambda x: pd.Series(x['keywords']), axis=1).stack().reset_index(level=1, drop=True)
    s.name = 'keyword'
    s = s.value_counts()
    s = s[s > 1]

    stemmer = SnowballStemmer('english')
    def filter_keywords(x):
        return [stemmer.stem(i) for i in x if i in s]

    df['keywords'] = df['keywords'].apply(filter_keywords)
    df['keywords'] = df['keywords'].apply(lambda x: [stemmer.stem(i) for i in x])
    df['keywords'] = df['keywords'].apply(lambda x: [str.lower(i.replace(' ', '')) for i in x])

    df['soup'] = df['keywords'] + df['cast'] + df['director'] + df['genres']
    df['soup'] = df['soup'].apply(lambda x: ' '.join(x))

    df.drop_duplicates(subset=['title', 'release_date'], keep='first', inplace=True)

    count = CountVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0.0, stop_words='english')
    count_matrix = count.fit_transform(df['soup'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)


    df = df.reset_index()
    indices = pd.Series(df.index, index=df['title'])

    data_path = './data/user_built/'
    if not os.path.exists(data_path):
        os.mkdir(data_path)

    with open(f"{data_path}/preprocessed_df.pkl", 'wb') as f:
        pickle.dump(df, f)

    with open(f"{data_path}/cosine_sim.pkl", 'wb') as f:
        pickle.dump(cosine_sim, f)

    with open(f"{data_path}/indices.pkl", 'wb') as f:
        pickle.dump(indices, f)

    with open(f"{data_path}/count_vectorizer.pkl", 'wb') as f:
        pickle.dump(count, f)