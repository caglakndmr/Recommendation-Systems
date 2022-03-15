# Made by caglakndmr @GitHub


# Dataset used
#
# https://www.kaggle.com/rounakbanik/the-movies-dataset

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
pd.set_option("display.expand_frame_repr", False)

df = pd.read_csv("the_movies_dataset/movies_metadata.csv", low_memory=False)    # DtypeWarning kapamak için
df.head()
df.shape

df["overview"].head()

# stop_words to delete words such as "the, a, in..."
tfidf = TfidfVectorizer(stop_words="english")

# to fill null values in "overview"
df[df["overview"].isnull()]
df["overview"] = df["overview"].fillna("")

tfidf_matrix = tfidf.fit_transform(df["overview"])
tfidf_matrix.shape

tfidf.get_feature_names()
tfidf_matrix.toarray()


# Cosine Similarity Matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
cosine_sim.shape
cosine_sim[1]


# Recommendations
indices = pd.Series(df_mini.index, index=df_mini["title"])
# many of one movie
indices.index.value_counts()
indices = indices[~indices.index.duplicated(keep="last")]
indices["Hamlet"]

movie_index = indices["Hamlet"]
cosine_sim[movie_index]
similarity_scores = pd.DataFrame(cosine_sim[movie_index], columns=["score"])

# Starting from 1, because 0 contains the movie itself
movie_indices = similarity_scores.sort_values("score", ascending=False)[1:11].index
df_mini["title"].iloc[movie_indices]
