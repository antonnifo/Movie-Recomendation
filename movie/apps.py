# movie/apps.py

from django.apps import AppConfig
from rich import print

class MovieConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movie'

    # References to data and models
    MOVIES = None            # Will store DataFrame of movie info
    RATING_ALGO = None       # Trained Surprise model
    MOVIEID_MAP = None       # Maps raw movieId (int) to Surprise internal IDs
    REVERSE_MOVIEID_MAP = None  # Maps Surprise internal IDs back to raw IDs
    VECTORIZER = None        # We'll add this for the TF-IDF vectorizer
    TFIDF_MATRIX = None      # We'll store the fitted TF-IDF matrix here

    def ready(self):
        """
        Called once when the Django application starts.
        Loads the Surprise built-in MovieLens-100k dataset, parses movie metadata 
        from u.item, trains a KNN-based item-item collaborative filtering model, 
        and stores them in class-level variables for global access.
        """
        import os
        import pandas as pd
        from surprise import Dataset, KNNWithMeans
        from surprise.model_selection import train_test_split
        from sklearn.feature_extraction.text import TfidfVectorizer
        from .helpers import clean_title

        # 1. Load built-in 'ml-100k' ratings (Downloads if not already present)
        data = Dataset.load_builtin('ml-100k')
        trainset = data.build_full_trainset()

        # 2. Parse local `u.item` to get movie metadata
        #    Surprise typically downloads data into `~/.surprise_data/ml-100k/ml-100k`
        surprise_data_dir = os.path.expanduser(
            "~/.surprise_data/ml-100k/ml-100k")
        u_item_path = os.path.join(surprise_data_dir, "u.item")

        cols = [
            "movieId", "title", "release_date", "video_release_date", "IMDb_URL",
            "unknown", "Action", "Adventure", "Animation", "Children's", "Comedy",
            "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror",
            "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"
        ]

        movies_df = pd.read_csv(
            u_item_path,
            sep='|',
            names=cols,
            encoding='latin-1'
        )

        # 3. Train a KNN-based item-item collaborative filtering model
        sim_options = {
            'name': 'pearson_baseline',
            'user_based': False  # item-based
        }
        algo = KNNWithMeans(sim_options=sim_options)
        algo.fit(trainset)


        # 4. Build a mapping from raw movieId to Surprise's internal IDs
        # MovieConfig.MOVIEID_MAP = trainset._raw2inner_id_items
        # MovieConfig.REVERSE_MOVIEID_MAP = trainset._inner2raw_id_items
        MovieConfig.RATING_ALGO = algo

        # 5. Store the movies DataFrame for global use
        MovieConfig.MOVIES = movies_df

        # -- NOW THE CONTENT-BASED PART --
        # 6. Clean the movie titles
        movies_df['clean_title'] = movies_df['title'].astype(
            str).apply(clean_title)

        # 7. Fit TF-IDF on the "clean_title" column
        vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform(movies_df['clean_title'])

        MovieConfig.VECTORIZER = vectorizer
        MovieConfig.TFIDF_MATRIX = tfidf_matrix
