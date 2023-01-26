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


def get_recomendations(user_film: dict, films: dict[dict], top: int = 8) -> list[str]:
    rating = {comparing_film['original_title']: calculate_points(user_film, comparing_film)
              for comparing_film in films
              if comparing_film != user_film}
    rating = dict(sorted(rating.items(), key=lambda f: f[1], reverse=True))
    return list(rating.keys())[:top]


def main():
    parser = ArgumentParser()
    parser.add_argument("--db",
                        default="films_db.json",
                        help="Путь к файлу с базой фильмов. По умолчанию films_db.json")
    args = parser.parse_args()

    with open(args.db, encoding='utf-8') as file:
        films = json.load(file)

    keyword = input("Enter film to search for: ")
    for film in films:
        if keyword == film['original_title']:
            user_film = film
            break
    else:
        print('No such film in FilmsDB')
        return

    recommendation = get_recomendations(user_film, films)
    for film in sorted(recommendation):
        print(film)


if __name__ == '__main__':
    main()
