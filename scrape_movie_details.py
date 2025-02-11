import requests
from dotenv import load_dotenv
import os
from time import sleep
import pandas as pd

load_dotenv()
api_key = os.getenv("API_KEY")


def create_url(movie_id) -> str:
    return (
        f"https://api.themoviedb.org/3/movie/{movie_id}?"
        + f"append_to_response={','.join(append_to_response)}&"
        + f"language={language}"
    )


def get_movie_details(movie_id: str) -> dict:
    url = create_url(movie_id)
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error: ", response.json())
        exit()

    return response.json()


language = "da-DK"
append_to_response = ["credits", "keywords"]

headers = {"accept": "application/json", "Authorization": f"Bearer {api_key}"}


movie_ids = pd.read_csv("movies.csv")["id"].tolist()

print(f"Scraping movie details for {len(movie_ids)} movies")

movie_details = []
for movie_id in movie_ids:
    movie_details.append(get_movie_details(movie_id))

    sleep(1 / 20)
    print(f"scraping movies details: {len(movie_details)}/{len(movie_ids)}", end="\r")

print(f"Finished scraping {len(movie_details)} movies\n")


# save to csv
df_movies = pd.DataFrame(movie_details)
df_movies.to_csv("movie_details.csv", index=False)
print(f"Saved movie details to movie_details.csv (total: {df_movies.shape[0]})")
