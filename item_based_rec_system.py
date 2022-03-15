# Made by caglakndmr @GitHub


# Dataset used
#
# https://grouplens.org/datasets/movielens/

import pandas as pd
pd.set_option("display.max_columns", 500)


movie = pd.read_csv("movie_lens_dataset/movie.csv")
rating = pd.read_csv("movie_lens_dataset/rating.csv")
df = movie.merge(rating, how="left", on="movieId")
df.head()
df.shape

df["title"].nunique()
df["title"].value_counts().head()

# comment counts on movies
comment_counts = pd.DataFrame(df["title"].value_counts())
# movies with less comments
rare_movies = comment_counts[comment_counts["title"] <= 1000].index
# movies with more comments
common_movies = df[~df["title"].isin(rare_movies)]
common_movies.shape

common_movies["title"].nunique()
df["title"].nunique()

# rows -> users, columns -> movies. pivot
user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
user_movie_df.shape
user_movie_df.columns



#Item-Based Recommendation
movie_name = "Ocean's Twelve (2004)"
movie_name = user_movie_df[movie_name]
user_movie_df.corrwith(movie_name).sort_values(ascending=False).head(10)

# random movie
movie_name = pd.Series(user_movie_df.columns).sample(1).values[0]


def check_film(keyword, user_movie_df):
    # movie search with keyword
    return [col for col in user_movie_df.columns if keyword in col]

check_film("Sherlock", user_movie_df)
check_film("Insomnia", user_movie_df)

