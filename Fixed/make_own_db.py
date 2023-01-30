import json
import os

import requests
from argparse import ArgumentParser
from dotenv import load_dotenv


def load_films(api_key: str, films_limit: int) -> list[dict]:
    all_films = []
    params = {
        "api_key": api_key,
        "language": "ru",
    }
    film_id = total_films = 0
    while True:
        url = f"https://api.themoviedb.org/3/movie/{film_id}"
        response = requests.get(url, params=params)
        if response.status_code == 401:
            raise requests.exceptions.HTTPError(response.json()["status_message"])
        elif response.status_code == 404:
            film_id += 1
            continue
        response.raise_for_status()

        all_films.append(response.json())
        film_id += 1
        total_films += 1
        if total_films == films_limit:
            return all_films


def main():
    load_dotenv()
    api_key = os.environ["TMDB_API_KEY"]
    parser = ArgumentParser()
    parser.add_argument("--FilmsLimit",
                        dest="films_limit",
                        type=int,
                        default=1000,
                        help="A number of films to load. By default is 1000.")
    parser.add_argument("--FilmsDB",
                        dest="db_file",
                        default="MyFilmDB.json",
                        help="The path to the movie database file for saving to. By default is MyFilmDB.json")
    args = parser.parse_args()

    print("Please wait. This operation may take about 15-20 minutes")
    with open(args.db_file, "w", encoding="utf-8") as db_file:
        json.dump(load_films(api_key, args.films_limit),
                  db_file,
                  ensure_ascii=False,
                  indent=4)


if __name__ == "__main__":
    main()
