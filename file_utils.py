from json import dump, load


def get_followed_mangas():
    with open('mangas.txt', 'r') as f:
        return f.read().splitlines()


def get_already_alerted_mangas():
    try:
        with open('mangas.json', 'r') as f:
            return load(f)
    except FileNotFoundError as e:
        open('mangas.json', 'w')
        return {}


def dump_already_alerted_mangas(mangas):
    with open('mangas.json', 'w') as f:
        dump(mangas, f)
