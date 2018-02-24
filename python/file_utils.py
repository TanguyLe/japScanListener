from json import dump, load
import os

path = os.path.dirname(os.path.abspath(__file__))


def get_followed_mangas():
    with open(path + '/../data/mangas.txt', 'r') as f:
        return f.read().splitlines()


def get_already_alerted_mangas():
    try:
        with open(path + '/../data/mangas.json', 'r') as f:
            return load(f)
    except FileNotFoundError as e:
        open(path + './data/mangas.json', 'w')
        return {}


def dump_already_alerted_mangas(mangas):
    with open(path + '/../data/mangas.json', 'w') as f:
        dump(mangas, f)
