from time import sleep
import argparse

from constants import *
from file_utils import get_already_alerted_mangas, get_followed_mangas
from full_process import full_process


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cron', action="store_true", help='Launch once for cron usage')
    args = parser.parse_args()

    cron_mode = args.cron

    # load followed mangas:
    followed_mangas = get_followed_mangas()

    # load already_alerted_mangas:
    already_alerted_mangas = get_already_alerted_mangas()

    if not cron_mode:
        while 1:
            full_process(already_alerted_mangas=already_alerted_mangas, followed_mangas=followed_mangas)

            sleep(SCRAPPING_TIMEOUT)

    else:
        full_process(already_alerted_mangas=already_alerted_mangas, followed_mangas=followed_mangas)


if __name__ == "__main__":
    main()
