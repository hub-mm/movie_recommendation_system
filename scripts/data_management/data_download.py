# ./scripts/data_download.py
import logging
import os
import kagglehub
import shutil


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def download_movie_data(dataset_path='./data/movies_dataset'):
    if not os.path.exists(dataset_path):
        logger.info(f"Making directories: {dataset_path}")
        os.makedirs(dataset_path)

    if not os.path.exists(f"{dataset_path}/7"):
        # Download from Kaggle: The Movie Dataset Path
        default_path = kagglehub.dataset_download("rounakbanik/the-movies-dataset")
        shutil.move(default_path, dataset_path)

    logger.info(f"Path to dataset file: {dataset_path}")

download_movie_data()