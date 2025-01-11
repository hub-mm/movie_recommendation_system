# ./scripts/top_chart/top_chart_collab_filtering.py
from scripts.data_management.data_preprocess_ratings import preprocess_ratings
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate
import os
import pickle


def build_model_filtering():
    reader = Reader()
    ratings = preprocess_ratings()
    data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

    svd = SVD(n_factors=50, n_epochs=100, lr_all=0.007, reg_all=0.005)

    print("Performing cross-validation...")
    cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=5, n_jobs=-1)

    print("Training the model on the full dataset...")
    train_set = data.build_full_trainset()
    svd.fit(train_set)

    print("Global mean rating:", train_set.global_mean)
    print("First 10 user biases:\n", svd.bu[:10])
    print("First 10 item biases:\n", svd.bi[:10])

    print("\nExample prediction for userId=1, movieId=1029 with actual rating=3:")
    svd.predict(uid=1, iid=1029, r_ui=3, verbose=True)
    svd.predict(uid=1, iid=628, r_ui=3, verbose=True)

    model_path = './model/'
    if not os.path.exists(model_path):
        os.mkdir(model_path)

    with open(f"{model_path}/model_filtering.pkl", 'wb') as f:
        pickle.dump(svd, f)

    return svd