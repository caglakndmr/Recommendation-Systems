# Made by caglakndmr @GitHub


# Dataset used
#
# https://grouplens.org/datasets/movielens/

import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
pd.set_option("display.expand_frame_repr", False)

def create_user_movie_df():
    movie = pd.read_csv("movie_lens_dataset/movie.csv")
    rating = pd.read_csv("movie_lens_dataset/rating.csv")
    df = movie.merge(rating, how="left", on="movieId")
    comment_counts = pd.DataFrame(df["title"].value_counts())
    rare_movies = comment_counts[comment_counts["title"] <= 1000].index
    common_movies = df[~df["title"].isin(rare_movies)]
    user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
    return user_movie_df

user_movie_df = create_user_movie_df()

random_user = int(pd.Series(user_movie_df.index).sample(1, random_state=45).values)



# Which movies did the user watch
random_user
user_movie_df
random_user_df = user_movie_df[user_movie_df.index == random_user]

# movies that have been rated
movies_watched = random_user_df.columns[random_user_df.notna().any()].tolist()
user_movie_df.loc[user_movie_df.index == random_user, user_movie_df.columns == "Silence of the Lambs, The (1991)"]

# how many movies have been watched
len(movies_watched)



# Other users who have watched the same movies
movies_watched_df = user_movie_df[movies_watched]

# should we include people who watched less movies?
# getting users who watched at least 20 of the same movies
user_movie_count = movies_watched_df.T.notnull().sum()
user_movie_count = user_movie_count.reset_index()
user_movie_count.columns = ["userId", "movie_count"]
user_movie_count[user_movie_count["movie_count"] > 20].sort_values("movie_count", ascending=False)
# users who have watched all the same movies
user_movie_count[user_movie_count["movie_count"] == 33].count()

users_same_movies = user_movie_count[user_movie_count["movie_count"] > 20]["userId"]



# Determining users, similar to the target user
final_df = pd.concat([movies_watched_df[movies_watched_df.index.isin(users_same_movies)],
                      random_user_df[movies_watched]])

corr_df = final_df.T.corr().unstack().sort_values().drop_duplicates()
corr_df = pd.DataFrame(corr_df, columns=["corr"])
corr_df.index.names = ["user_id_1", "user_id_2"]
corr_df = corr_df.reset_index()

# 65% and above correlation with target user
top_users = corr_df[(corr_df["user_id_1"] == random_user) & (corr_df["corr"] >= 0.65)][["user_id_2", "corr"]].reset_index(drop=True)
top_users = top_users.sort_values(by="corr", ascending=False)
top_users.rename(columns={"user_id_2": "userId"}, inplace=True)

rating = pd.read_csv("movie_lens_dataset/rating.csv")
top_users_rating = top_users.merge(rating[["userId", "movieId", "rating"]], how="inner")

top_users_rating = top_users_rating[top_users_rating["userId"] != random_user]


# Weighted Average Recommendation Score
top_users_rating['weighted_rating'] = top_users_rating['corr'] * top_users_rating['rating']
top_users_rating.groupby('movieId').agg({"weighted_rating": "mean"})

recommendation_df = top_users_rating.groupby('movieId').agg({"weighted_rating": "mean"})
recommendation_df = recommendation_df.reset_index()
recommendation_df[recommendation_df["weighted_rating"] > 3.5]

movies_to_be_recommend = recommendation_df[recommendation_df["weighted_rating"] > 3.5].sort_values("weighted_rating", ascending=False)

movie = pd.read_csv('movie_lens_dataset/movie.csv')
movies_to_be_recommend.merge(movie[["movieId", "title"]])

