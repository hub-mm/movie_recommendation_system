# ./scripts/top_chart/top_chart_similar.py
from scripts.data_management.data_preprocess_movies_metadata import preprocess
from scripts.data_management.data_preprocess_credits import preprocess_credits
from scripts.data_management.data_preprocess_keywords import preprocess_keywords
import pandas as pd
import numpy as np
from ast import literal_eval
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_similar_chart(title='batman', amount=30):
    title = title.lower()
    df = preprocess()

    vote_counts = df[df['vote_count'].notnull()]['vote_count'].astype('float')
    min_votes = vote_counts.quantile(0.50)

    df = df[
        (df['vote_count'].astype('float') >= min_votes) & (df['vote_count'].notnull()) & (df['vote_average'].notnull())
        ][
        ['title', 'release_date', 'vote_count', 'vote_average', 'popularity', 'genres', 'tagline', 'overview', 'id']
    ]

    df['title'] = df['title'].fillna('').str.lower()
    indices = pd.Series(df.index, index=df['title'])

    if title not in indices:
        print(f"Title '{title}' not found!")
        return

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

    def get_directors(x):
        for i in x:
            if i['job'] == 'Director':
                return i['name']
        return np.nan

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
        words = []
        for i in x:
            if i in s:
                words.append(i)

        return words

    df['keywords'] = df['keywords'].apply(filter_keywords)
    df['keywords'] = df['keywords'].apply(lambda x: [stemmer.stem(i) for i in x])
    df['keywords'] = df['keywords'].apply(lambda x: [str.lower(i.replace(' ', '')) for i in x])

    df['soup'] = df['keywords'] + df['cast'] + df['director'] + df['genres']
    df['soup'] = df['soup'].apply(lambda x: ' '.join(x))

    count = CountVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0.0, stop_words='english')
    count_matrix = count.fit_transform(df['soup'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    df = df.reset_index()
    indices = pd.Series(df.index, index=df['title'])

    val = indices[title]
    if isinstance(val, pd.Series):
        idx = val.iloc[0]
    else:
        idx = val

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:amount + 1]

    movie_indices = [i[0] for i in sim_scores]
    cols_to_show = ['title', 'release_date', 'vote_count', 'vote_average', 'popularity', 'genres', 'cast']
    df['title'] = df['title'].fillna('').str.title()

    return df.iloc[movie_indices][cols_to_show]