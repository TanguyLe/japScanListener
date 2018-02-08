class Manga:
    def __init__(self, title=None, chapters_types=None, chapters_links=None, chapters_numbers=None, dict=None):
        if not (dict or (title and chapters_types and chapters_links and chapters_numbers)):
            raise TypeError("Manga must be constructed either by a dict or the parameters")

        if dict:
            self.title = dict['title']
            self.chapters_types = dict['chapters_types']
            self.chapters_numbers = dict['chapters_numbers']
            self.chapters_links = dict['chapters_links']
        else:
            self.title = title
            self.chapters_types = chapters_types
            self.chapters_numbers = chapters_numbers
            self.chapters_links = chapters_links

    def serialize_chapter(self, index):
        r_str = str(self.chapters_numbers[index]) + ": " + self.chapters_types[index] + " at "
        r_str += self.chapters_links[index] + '\n'

        return r_str

    def serialize(self):
        r_str = self.title + ':\n'
        for i in range(len(self.chapters_numbers)):
            r_str += self.serialize_chapter(i)

        return r_str
