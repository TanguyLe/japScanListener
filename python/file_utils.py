from json import dump, load
import os

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
MANGAS_PATH = os.path.join(os.path.dirname(CURRENT_PATH), "data", "mangas")
MANGAS_TXT = MANGAS_PATH + ".txt"
MANGAS_JSON = MANGAS_PATH + ".json"


def get_followed_mangas():
    with open(MANGAS_TXT, 'r') as f:
        return f.read().splitlines()


def get_already_alerted_mangas():
    try:
        with open(MANGAS_JSON, 'r') as f:
            return load(f)
    except FileNotFoundError:
        with open(MANGAS_JSON, 'w') as f:
            dump({}, f)
        return {}


def dump_already_alerted_mangas(mangas):
    with open(MANGAS_JSON, 'w') as f:
        dump(mangas, f)
