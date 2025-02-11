import requests
from dotenv import load_dotenv
import os
from time import sleep
import pandas as pd

load_dotenv()
api_key = os.getenv("API_KEY")


def create_url(release_year: int, page: int) -> str:
    return (
        "https://api.themoviedb.org/3/discover/movie"
        "?include_adult=false"
        "&include_video=false"
        f"&page={page}"
        f"&primary_release_year={release_year}"
        "&sort_by=popularity.desc"
        f"&language={language}"
        f"&with_origin_country={origin_country}"
        f"&with_original_language={original_language}"
    )


def get_page_results(url: str) -> dict:
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error: ", response.json())
        exit()

    return response.json()


def get_total_pages(url: str) -> int:
    response = get_page_results(url)
    return response["total_pages"]


def get_movies_from_year(year: int) -> list:
    total_pages = get_total_pages(create_url(year, 1))
    movies = []
    for page in range(1, total_pages + 1):
        url = create_url(year, page)
        response = get_page_results(url)
        movies.extend(response["results"])
    return movies


language = "da-DK"
origin_country = language.split("-")[1]
original_language = language.split("-")[0]

headers = {"accept": "application/json", "Authorization": f"Bearer {api_key}"}


movies = []
for year in range(1897, 2030):
    movies.extend(get_movies_from_year(year))
    print(f"scraping movies: {len(movies)}", end="\r")

print(f"Finished scraping {len(movies)} movies\n")


# save to csv
df_movies = pd.DataFrame(movies)
df_movies.to_csv("movies.csv", index=False)
print(f"Saved movies to movies.csv (total: {df_movies.shape[0]})")
