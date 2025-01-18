import pandas as pd
import requests
import os
import pickle
from concurrent.futures import ThreadPoolExecutor, as_completed


def is_valid_url(url, timeout=5):
    try:
        response = requests.head(url, allow_redirects=True, timeout=timeout)
        return response.status_code == 200
    except requests.RequestException:
        return False


def preprocess_movies_with_valid_posters(
        filepath='./data/movies_dataset/7/movies_metadata.csv',
        base_url='https://image.tmdb.org/t/p/w500',
        max_workers=20
):
    df = pd.read_csv(filepath, dtype='unicode')
    df['poster_path'] = df['poster_path'].fillna('').astype(str).str.strip()
    df['full_url'] = base_url + df['poster_path']

    print("Total movies before filtering:", len(df))

    def check_row(idx, row):
        if row['poster_path'] == "":
            return None
        url = row['full_url']
        if is_valid_url(url):
            return row
        return None

    valid_rows = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_row, idx, row): idx for idx, row in df.iterrows()}

        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                valid_rows.append(result)

    filtered_df = pd.DataFrame(valid_rows)
    print("Total movies after filtering:", len(filtered_df))
    return filtered_df


def get_filtered_movies():
    data_path = './data/user_built/'
    if not os.path.exists(data_path):
        os.mkdir(data_path)

    filtered_df = preprocess_movies_with_valid_posters()
    pickle_path = os.path.join(data_path, "preprocessed_df_movies.pkl")
    with open(pickle_path, 'wb') as f:
        pickle.dump(filtered_df, f)

    print("Filtered DataFrame saved to", pickle_path)
    return filtered_df


if __name__ == "__main__":
    df_valid = get_filtered_movies()
    print(df_valid[['title', 'poster_path', 'full_url']].head())