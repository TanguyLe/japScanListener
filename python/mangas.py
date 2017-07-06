class Manga:
    def __init__(self, title, chapters_types, links, chapter_numbers):
        self.title = title
        self.chapters_types = chapters_types
        self.chapter_numbers = chapter_numbers
        self.links = links

    def serialize(self):
        chapters_types = ""

        for chapt_type in self.chapters_types:
            chapters_types += chapt_type + ","

        chapters_types = chapters_types[-1]

        return self.title + ", de type(s) : " + chapters_types
