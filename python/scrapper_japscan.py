from bs4 import BeautifulSoup
from re import search

from constants import VF_REGEX, FR_TYPE, JAPSCAN_URL


class JapScanScrapper:
    def __init__(self, content):
        soup = BeautifulSoup(content, "lxml")

        self.div = soup.find(name="div", text="Aujourd'hui")
        if not self.div:
            self.div = soup.find(name="div", text="Hier")

        self.div = self.div.next_sibling

    def until_next_date_condition(self):
        return "date" not in self.div.get('class')

    def get_chapters_div_from_manga(self):
        if self.div.next_sibling.get('class') and ("hot" in self.div.next_sibling.get('class')):
            chapters_div = self.div.next_sibling.next_sibling
        else:
            chapters_div = self.div.next_sibling

        return chapters_div

    def next_manga_from_manga(self):
        if self.div.next_sibling.get('class') and ("hot" in self.div.next_sibling.get('class')):
            self.div = self.div.next_sibling.next_sibling.next_sibling
        else:
            self.div = self.div.next_sibling.next_sibling

    def get_cursor(self):
        return self.div

    def get_mangas(self):
        mangas = []

        while self.until_next_date_condition():

            chapters_list = self.get_chapters_div_from_manga().contents

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

            manga = dict()
            manga['title'] = self.get_cursor().text
            manga['chapters_types'] = list_chapter_types
            manga['chapters_links'] = list_chapter_links
            manga['chapters_numbers'] = list_chapter_numbers

            mangas.append(manga)

            self.next_manga_from_manga()

        return mangas

