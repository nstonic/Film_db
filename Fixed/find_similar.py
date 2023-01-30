import json

from argparse import ArgumentParser


def calculate_points(user_film: dict, comparing_film: dict) -> int:
    param_points = {
        "belongs_to_collection": 1000,
        "original_language": 300,
        "budget": 100,
        "genres": 500
    }
    return sum(param_points[param]
               for param in param_points
               if comparing_film[param] == user_film[param])


def get_recommendations(user_film: dict, films: dict[dict]) -> list[tuple[str, int]]:
    ratings = {
        comparing_film["original_title"]: calculate_points(user_film, comparing_film)
        for comparing_film in films
        if comparing_film != user_film
    }

    return sorted(
        ratings.items(),
        key=lambda rating: rating[1],
        reverse=True
    )


def main():
    parser = ArgumentParser()
    parser.add_argument("--FilmsDB",
                        dest="db_file",
                        default="MyFilmDB.json",
                        help="The path to the movie database file. By default is MyFilmDB.json")
    parser.add_argument("--top",
                        type=int,
                        default=8,
                        help="The number of recommendations to output. By default is 8")
    args = parser.parse_args()

    with open(args.db_file, encoding="utf-8") as file:
        films = json.load(file)

    desired_title = input("Enter a film title to search for: ")
    try:
        user_film = next(filter(lambda film: film["original_title"] == desired_title, films))
    except StopIteration:
        print(f"No such film in {args.db_file}")
        return

    recommendations = get_recommendations(user_film, films)
    max_points = 1900
    for index, recommendation in enumerate(recommendations[:args.top]):
        print(f"{index + 1}) {recommendation[0]} - matching {recommendation[1] / max_points:.0%}")


if __name__ == "__main__":
    main()
