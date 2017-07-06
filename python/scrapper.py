from bs4 import BeautifulSoup


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
