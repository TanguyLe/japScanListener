from datetime import datetime
from email_utils import SmtpLink

from constants import *
from mangas import Manga
from requests import get
from scrapper_japscan import JapScanScrapper
from scrapper_mangakakalot import MangakakalotScrapper
from file_utils import dump_already_alerted_mangas

from private_config import PERSONS


def full_process(already_alerted_mangas, followed_mangas, cron=False):
    now_orig = datetime.now()

    print(SCRAPPING_STARTS.format(date=now_orig.strftime("%b %d"), time=now_orig.strftime("%Hh%M")))

    try:
        result_japscan = get(JAPSCAN_URL)
        content_japscan = result_japscan.content

        scrapper_japscan = JapScanScrapper(content_japscan)

        result_mangakakalot = get(MANGAKAKALOT_URL)
        content_mangakakalot = result_mangakakalot.content

        scrapper_mangakakalot = MangakakalotScrapper(content_mangakakalot)

        mangas_to_watch = [Manga(dict=m) for m in (scrapper_japscan.get_mangas() + scrapper_mangakakalot.get_mangas())]
        msg = ""

        for manga in mangas_to_watch:
            if manga.title in followed_mangas:
                for idx, chapter_type in enumerate(manga.chapters_types):
                    if (chapter_type not in [RAW_TYPE, SPOILER_TYPE] and
                            (manga.title not in already_alerted_mangas.keys() or
                                     manga.chapters_numbers[idx] > already_alerted_mangas[manga.title])):
                        already_alerted_mangas[manga.title] = manga.chapters_numbers[idx]
                        msg += manga.title + " "
                        msg += manga.serialize_chapter(idx)
        if msg:
            mail_server = SmtpLink.create_service()

            dump_already_alerted_mangas(already_alerted_mangas)

            str_msg = SmtpLink.get_string_email(msg=msg,
                                                subject=SUBJECT,
                                                origin=ORIGIN,
                                                destination=DESTINATION)
            print(SENDING_EMAILS)
            print(msg)

            mail_server.send_mail(to_addrs=PERSONS, msg=str_msg)

            mail_server.close()

        now_end = datetime.now()
        delta = now_end - now_orig

        print(SCRAPPING_COMPLETED.format(date=now_orig.strftime("%b %d"), delta=str(delta.total_seconds() * 100)[0:4]))

    except Exception as e:
        print(SCRAPPING_FAILED.format(date=now_orig.strftime("%b %d"), error=str(e)))
