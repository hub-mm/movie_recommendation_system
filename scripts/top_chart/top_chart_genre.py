# ./scripts/top_chart/top_chart_genre.py
from scripts.data_management.data_preprocess_movies_metadata import preprocess_movies_md
import pandas as pd


def movies_sorted_genre():
    df = preprocess_movies_md()
    s = df.apply(lambda x: pd.Series(x['genres']), axis=1).stack().reset_index(level=1, drop=True)
    s.name = 'genre'
    gen_df = df.drop('genres', axis=1).join(s)

    return gen_df

def build_genre_chart(genre, top_chart_num=250):
    df = movies_sorted_genre()
    df = df[df['genre'] == genre.capitalize()]

    vote_counts = df[df['vote_count'].notnull()]['vote_count'].astype('float')
    vote_av = df[df['vote_average'].notnull()]['vote_average'].astype('float')
    vote_av_mean = vote_av.mean()
    min_votes = vote_counts.quantile(0.85)

    qualified = df[
        (df['vote_count'].astype('float') >= min_votes) & (df['vote_count'].notnull()) & (df['vote_average'].notnull())
        ][
        ['title', 'release_date', 'vote_count', 'vote_average', 'popularity']
    ]
    qualified['vote_count'] = qualified['vote_count'].astype('float')
    qualified['vote_average'] = qualified['vote_average'].astype('float')

    qualified['wr'] = qualified.apply(
        lambda x: (
        x['vote_count'] / (x['vote_count'] + min_votes) * x['vote_average']) + (min_votes / (min_votes + x['vote_count']) * vote_av_mean),
        axis=1
    )

    qualified = qualified.sort_values('wr', ascending=False).head(top_chart_num)

    return qualified