# ./scripts/top_chart/top_chart_rating.py
from scripts.data_management.data_preprocess_movies_metadata import preprocess_movies_md


def build_top_chart(top_chart_num=250, amount=10):
    df = preprocess_movies_md()

    vote_counts = df[df['vote_count'].notnull()]['vote_count'].astype('float')
    vote_av = df[df['vote_average'].notnull()]['vote_average'].astype('float')
    vote_av_mean = vote_av.mean()
    min_votes = vote_counts.quantile(0.95)

    qualified = df[
        (df['vote_count'].astype('float') >= min_votes) & (df['vote_count'].notnull()) & (df['vote_average'].notnull())
    ][
        ['title', 'release_date', 'vote_count', 'vote_average', 'popularity', 'genres', 'poster_path']
    ]
    base_url = 'https://image.tmdb.org/t/p/w500'
    qualified['poster_path'] = base_url + qualified['poster_path'].astype(str)

    qualified['vote_count'] = qualified['vote_count'].astype('float')
    qualified['vote_average'] = qualified['vote_average'].astype('float')

    qualified['wr'] = qualified.apply(
        lambda x: (
        x['vote_count'] / (x['vote_count'] + min_votes) * x['vote_average']) + (min_votes / (min_votes + x['vote_count']) * vote_av_mean),
        axis=1
    )
    qualified = qualified.sort_values('wr', ascending=False).head(top_chart_num)

    qualified = qualified.head(amount).to_dict(orient='records')

    return qualified