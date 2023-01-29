import json

from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument("--FilmsDB",
                        dest="db_file",
                        default="MyFilmDB.json",
                        help="The path to the movie database file. By default is MyFilmDB.json")
    args = parser.parse_args()
    with open(args.db_file, encoding="utf-8") as file:
        films = json.load(file)

    keyword = input("Enter a keyword to search for: ")
    founded_films = list(filter(lambda film: keyword in film["original_title"], films))
    for film in founded_films:
        print(film["original_title"])


if __name__ == '__main__':
    main()
