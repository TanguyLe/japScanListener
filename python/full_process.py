import logging

from email_utils import SmtpLink
from constants import *
from mangas import Manga
from requests import get
from scrapper_japscan import JapScanScrapper
from scrapper_mangakakalot import MangakakalotScrapper
from file_utils import dump_already_alerted_mangas

from private_config import PERSONS


def full_process(already_alerted_mangas, followed_mangas, cron=False):

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler(LOG_PATH)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', DATE_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.info(SCRAPPING_STARTS)

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
            logger.info(SENDING_EMAILS)
            logger.info(msg)

            mail_server.send_mail(to_addrs=PERSONS, msg=str_msg)

            mail_server.close()

        logger.info(SCRAPPING_COMPLETED)

    except Exception as e:
        logger.info(SCRAPPING_FAILED.format(error=str(e)))
