from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('headless')

wd = webdriver.Chrome('./chromedriver.exe', chrome_options=options)

def getPageHTML(url):
    """
    Fetches the specified page's HTML data.
    :param url: URL of page to fetch
    :return: HTML of page
    """

    wd.get(url)

    if "CAPTCHA" in wd.page_source:
        print("Google is asking for a CAPTCHA. Please complete it.")
        input("Press ENTER when done.")

    return wd.page_source