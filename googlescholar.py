import re

class ScholarParse(object):
    """
    Parses HTML into a ScholarArticle
    """

    def parse(self, html):
        """
        Main logic - extracts and parses fields into ScholarArticle
        :param html:
        :return: parsed ScholarArticle
        """

        article = ScholarArticle()
        fields = self.getFields(html)

        for field in fields:
            key, value = field
            self.parseField(key, value, article)
        return article

    def getFields(self, html):
        """
        Get fields from Google Scholar page
        :param html:
        :return:
        """
        return re.findall('<div class="gs_scl"><div class="gsc_field">(.*?)<\/div><div class=".*?">(.*?)<\/div><\/div>', html)


    def parseField(self, key, value, article):
        """
        Parse Google Scholar field into ScholarArticle based on type
        :param key:
        :param value:
        :param article:
        :return:
        """
        if key == "Authors":
            article.authors = value.split(", ")
        elif key == "Publication date":
            article.publicationDate = value
        elif key == "Conference":
            article.conference = value
        elif key == "Description":
            article.description = self.stripHTML(value)
        elif key == "Total citations":
            article.citations = self.parseCitations(value)[0]


    def parseCitations(self, string):
        """
        Parses citation HTML block
        :param string: HTML from citations field
        :return: Number of citations
        """
        return re.findall(">Cited by (.*?)<", string)

    def stripHTML(self, string):
        """
        Remove any HTML tags from within the description
        :param string:
        :return: string without HTML tags
        """
        return re.sub("<.*?>", "", string)

class ScholarArticle(object):
    """
    Data structure for a Google Scholar article
    """
    def __init__(self):
        self.authors = []
        self.publicationDate = None
        self.conference = None
        self.publisher = None
        self.description = None
        self.citations = 0
        self.pages = None

    def __str__(self):
        return """
    Authors: {}
    Publication Date: {}
    Conference: {}
    Pages: {}
    Publisher: {}
    Description: {}
    Citations: {}
        """.format(
            self.authors,
            self.publicationDate,
            self.conference,
            self.pages,
            self.publisher,
            self.description,
            self.citations
        )

    def getDict(self):
        return {
            "Authors": self.authors,
            "Publication Date": self.publicationDate,
            "Conference": self.conference,
            "Pages": self.pages,
            "Publisher": self.publisher,
            "Description": self.description,
            "Citations": self.citations
        }

    @staticmethod
    def getCSVHeader():
        return "Authors\tPublication Date\tPublisher\tDescription\tCitations\n"

    def getCSV(self):
        return "{}\t{}\t{}\t{}\t{}\n".format(
            ", ".join(self.authors),
            self.publicationDate,
            self.publisher,
            self.description,
            self.citations
        )