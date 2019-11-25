from bs4 import BeautifulSoup
from re import search

import os

from constants import VF_REGEX, FR_TYPE, JAPSCAN_URL


class JapScanScrapper:
    def __init__(self, content):
        self.soup = BeautifulSoup(content, "lxml")

    @staticmethod
    def get_manga_title(divs_iter):
        return next(divs_iter).contents[1].text

    @staticmethod
    def get_chapters_list(divs_iter):
        next(divs_iter)

        return [c for c in next(divs_iter).contents if c != '\n']

    def get_mangas(self):
        mangas = []

        try:
            for i in range(1, 9):
                current_tab = self.soup.find(name="div", id="tab-" + str(i))
                mangas_list_it = current_tab.children

                for _ in mangas_list_it:
                    try:
                        manga_title = self.get_manga_title(mangas_list_it)
                    except StopIteration:
                        # Happens at the bottom of the page
                        break

                    list_chapter_types = []
                    list_chapter_links = []
                    list_chapter_numbers = []

                    for chapter in self.get_chapters_list(mangas_list_it):
                        chapter_div = chapter.contents[1]
                        chapter_text = chapter_div.text
                        chapter_number = int(search(VF_REGEX, str(chapter_text)).group(1))
                        chapter_link = chapter_div.get('href')

                        if len(chapter.contents) == 4:
                            chapter_type_str = chapter.contents[3].text.strip()
                        else:
                            chapter_type_str = FR_TYPE

                        list_chapter_links.append(os.path.join(JAPSCAN_URL, chapter_link))
                        list_chapter_types.append(chapter_type_str)
                        list_chapter_numbers.append(chapter_number)

                    manga = dict()
                    manga['title'] = manga_title
                    manga['chapters_types'] = list_chapter_types
                    manga['chapters_links'] = list_chapter_links
                    manga['chapters_numbers'] = list_chapter_numbers

                    mangas.append(manga)

            return mangas
        except Exception as e:
            raise(Exception("Scrapper_japscan failed: " + str(e)))

