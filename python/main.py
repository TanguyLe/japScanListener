from datetime import datetime
from re import search
from time import sleep

from constants import *
from email_utils import SmtpLink
from file_utils import get_already_alerted_mangas, get_followed_mangas, dump_already_alerted_mangas
from mangas import Manga
from requests import get
from scrapper import JapScanScrapper

from private_config import ME

# load followed mangas:
followed_mangas = get_followed_mangas()

# load already_alerted_mangas:
already_alerted_mangas = get_already_alerted_mangas()

while 1:
    sleep(SCRAPPING_TIMEOUT)

    now_orig = datetime.now()

    print(SCRAPPING_STARTS.format(time=now_orig.strftime("%Hh%M")))

    result = get(JAPSCAN_URL)
    content = result.content

    scrapper = JapScanScrapper(content)

    mangas_to_watch = []

    while scrapper.until_next_date_condition():

        chapters_list = scrapper.get_chapters_div_from_manga().contents

        list_chapter_types = []
        list_chapter_links = []
        list_chapter_numbers = []

        for chapter in chapters_list:
            chapter_contents = chapter.contents

            chapter_number = int(search(VF_REGEX, str(chapter_contents[0])).group(1))

            if len(chapter_contents) == 2:
                chapter_type_str = chapter_contents[1].text.strip()
            else:
                chapter_type_str = FR_TYPE

            list_chapter_links.append(JAPSCAN_URL + chapter_contents[0].get('href'))
            list_chapter_types.append(chapter_type_str)
            list_chapter_numbers.append(chapter_number)

        manga = Manga(scrapper.get_cursor().text, list_chapter_types, list_chapter_links, list_chapter_numbers)

        mangas_to_watch.append(manga)

        scrapper.next_manga_from_manga()

    msg = ""

    for manga in mangas_to_watch:
        if manga.title in followed_mangas:
                for idx, chapter_type in enumerate(manga.chapters_types):
                    if (chapter_type not in [RAW_TYPE, SPOILER_TYPE] and
                            (manga.title not in already_alerted_mangas.keys() or
                                manga.chapter_numbers[idx] > already_alerted_mangas[manga.title])):
                        already_alerted_mangas[manga.title] = manga.chapter_numbers[idx]
                        msg += LINE_MSG.format(title=manga.title, link=manga.links[idx])

    if msg:
        mail_server = SmtpLink.create_service()

        dump_already_alerted_mangas(already_alerted_mangas)

        str_msg = SmtpLink.get_string_email(msg=msg,
                                            subject=SUBJECT,
                                            origin=ORIGIN,
                                            destination=DESTINATION)
        print(SENDING_EMAILS)
        mail_server.send_mail(to_addrs=ME, msg=str_msg)
        # mail_server.send_mail(to_addrs=[GAUTIER, ME], msg=str_msg)

        mail_server.close()

    now_end = datetime.now()
    delta = now_end - now_orig

    print(SCRAPPING_COMPLETED.format(delta=str(delta.total_seconds() * 100)[0:4]))
