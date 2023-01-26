import json

from argparse import ArgumentParser


def calculate_points(user_film: dict, comparing_film: dict) -> int:
    param_points = {
        'belongs_to_collection': 1000,
        'original_language': 300,
        'budget': 100,
        'genres': 500
    }
    return sum(param_points[param]
               for param in param_points
               if comparing_film[param] == user_film[param])


def get_recommendations(user_film: dict, films: dict[dict], top: int = 8) -> list[str]:
    ratings = {comparing_film['original_title']: calculate_points(user_film, comparing_film)
               for comparing_film in films
               if comparing_film != user_film}
    ratings = dict(sorted(ratings.items(), key=lambda rating: rating[1], reverse=True))
    return list(ratings.keys())[:top]


def main():
    parser = ArgumentParser()
    parser.add_argument("--FilmsDB",
                        dest="db_file",
                        default="MyFilmDB.json",
                        help="Путь к файлу с базой фильмов. По умолчанию MyFilmDB.json")
    args = parser.parse_args()

    with open(args.db_file, encoding='utf-8') as file:
        films = json.load(file)

    desired_title = input("Enter film to search for: ")
    user_film = next((filter(lambda film: film["original_title"] == desired_title, films)), None)
    if not user_film:
        print('No such film in FilmsDB')
        return

    recommendations = get_recommendations(user_film, films)
    for film in sorted(recommendations):
        print(film)


if __name__ == '__main__':
    main()
