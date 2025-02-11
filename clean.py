import pandas as pd
import ast

columns = [
    "genre_ids",
    "id",
    "original_language",
    "original_title",
    "overview",
    "popularity",
    "release_date",
    "title",
    "vote_average",
    "vote_count",
]

df_movies = pd.read_csv("movies_details.csv")

print(df_movies.columns)
print(df_movies["id"].head())
exit()

df_movies = df_movies[columns]

# cast to correct values
df_movies["id"] = df_movies["id"].astype(int)
df_movies["popularity"] = df_movies["popularity"].astype(float)
df_movies["release_date"] = pd.to_datetime(df_movies["release_date"])
df_movies["vote_average"] = df_movies["vote_average"].astype(float)
df_movies["vote_count"] = df_movies["vote_count"].astype(int)
df_movies["genre_ids"] = df_movies["genre_ids"].apply(ast.literal_eval)

print(df_movies.head())

df_movies.to_csv("movies_clean.csv", index=False)
