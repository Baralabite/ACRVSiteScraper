import re
import util
from googlescholar import ScholarParse
import progressbar, time, random, html

#======================[ Scrape this page! ]======================#
PAGE_TO_SCRAPE = "https://www.roboticvision.org/publications/?y=2016"
#=================================================================#

class ACRVScraper:
    def __init__(self, page):
        self.pageURL = page

    def scrape(self):
        """
        Program logic
        :return:
        """
        pageHTML = self.getPageHTML(self.pageURL)
        urls = self.getGoogleScholarURLs(pageHTML)
        parser = ScholarParse()

        totalArticles = len(urls)
        print("Articles to parse: {}".format(totalArticles))

        self.bar = progressbar.ProgressBar(redirect_stdout=True)
        self.bar.min_value = 0
        self.bar.max_value = len(urls)

        articles = []

        #=====[ This is where the magic happens - iterates over google scholar URLs and parse them ]=====#
        for url in urls:
            #Get article HTML and parse it
            articleHTML = self.getPageHTML(html.unescape(url))
            article = parser.parse(articleHTML)

            #Add parsed article to list
            articles.append(article)

            #Update progress bar
            itemIndex = urls.index(url)
            self.bar.update(itemIndex)

            #Sleep for random time between 0.5s and 1.5s to try and circumvent query limits
            #time.sleep(random.randint(5, 15) / 10)

        #Writes output to CSV
        self.writeCSV(articles)

    def writeCSV(self, articles):
        """
        Write articles to a CSV file
        CSV delimited by tab (\t)
        :param articles:
        :return:
        """
        csvHeader = articles[0].getCSVHeader()

        with open("output.csv", "w") as file:
            file.write(csvHeader)
            for article in articles:
                file.write(article.getCSV())


    def getPageHTML(self, url):
        """
        Fetches the specified page's HTML data.
        Be warned this doesn't work for pages that use AJAX to load more entries after page has finished loading.
        This is currently not an issue in the QUT page.
        If this becomes a problem in the future, we can rewrite the script using Selenium.
        :param url: URL of page to fetch
        :return: HTML of page
        """
        return util.getPageHTML(url)

    def getGoogleScholarURLs(self, html):
        """
        Scrapes any links to Google Scholar from the page
        :param html: Page HTML to scrape
        :return: List of URLs to Google Scholar
        """
        return re.findall('<a .*?href="(https?://scholar.google.com.au\/.*?)".*?>', html)



if __name__ == "__main__":
    print("""ACRV Citation Scraper
==========================

    """)
    scraper = ACRVScraper(PAGE_TO_SCRAPE)
    scraper.scrape()