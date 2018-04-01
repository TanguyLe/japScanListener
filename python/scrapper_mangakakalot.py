from bs4 import BeautifulSoup
from re import search

from constants import CHAPTER_NUMBER_REGEX, US_TYPE


class MangakakalotScrapper:
    def __init__(self, content):
        soup = BeautifulSoup(content, "lxml")

        self.div = soup.find(name="div", class_="doreamon")

        self.div = self.div.contents[1]

    def until_next_date_condition(self):
        return self.div and len(self.div.contents)

    def get_chapters_div_from_manga(self):
        chapters_list_div = self.div.contents[3]

        return chapters_list_div.contents

    def next_manga_from_manga(self):
        if (self.div.next_sibling and self.div.next_sibling.next_sibling
            and self.div.next_sibling.next_sibling.get('class') and
                ("rowitemupdate" in self.div.next_sibling.next_sibling.get('class')) and
                self.div.next_sibling.next_sibling.next_sibling):
            self.div = self.div.next_sibling.next_sibling.next_sibling.next_sibling
        else:
            self.div = self.div.next_sibling.next_sibling

    def get_cursor(self):
        return self.div

    def get_mangas(self):
        mangas = []
        chapter_number_text = ""

        try:
            while self.until_next_date_condition():

                chapters_list_inter = self.get_chapters_div_from_manga()
                chapters_list = chapters_list_inter[3:]

                list_chapter_types = []
                list_chapter_links = []
                list_chapter_numbers = []

                for chapter in filter(lambda c: c != "\n", chapters_list):
                    chapter_link_div = chapter.contents[1].contents[0]
                    chapter_number_text = chapter_link_div.text.strip()

                    chapter_number = int(search(CHAPTER_NUMBER_REGEX, chapter_number_text).group(2))

                    list_chapter_links.append(chapter_link_div.get('href'))
                    list_chapter_types.append(US_TYPE)
                    list_chapter_numbers.append(chapter_number)

                manga = dict()
                manga['title'] = chapters_list_inter[1].contents[1].contents[0].text
                manga['chapters_types'] = list_chapter_types
                manga['chapters_links'] = list_chapter_links
                manga['chapters_numbers'] = list_chapter_numbers

                mangas.append(manga)

                self.next_manga_from_manga()

            return mangas

        except Exception as e:
            raise(Exception("Scrapper_mangakakalot failed (on " + str(chapter_number_text) + "): " + str(e)))
