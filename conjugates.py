from main import create_page
from bs4 import SoupStrainer
from bs4 import BeautifulSoup as bs


class TenseRow(object):
    def __init__(self, row):
        self.row = row


class TenseConjugates(object):
    def __init__(self, page):
        self.page = page

    def __str__(self):
        return self.page.prettify()

    def cos(self):
        strainer = SoupStrainer(class_='vtable-body-row')
        return bs(self.page.prettify(),
                  'html.parser', parse_only=strainer)



def conjugation(word):
    url = 'http://www.spanishdict.com/conjugate/'
    strainer = SoupStrainer(class_='conjugation')
    page = create_page(word, url, to_print=False, strainer=strainer)
    # print(create_page(word, url, to_print=False).prettify())
    a = TenseConjugates(page)
    print(a.cos())


if __name__ == '__main__':
    conjugation('coger')
