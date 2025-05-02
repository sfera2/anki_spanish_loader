import urllib.parse
from urllib.parse import quote
import urllib.request
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer


def create_page(word, url, to_print, strainer=None):
    req = urllib.request.Request(url + quote(word))
    with urllib.request.urlopen(req) as response:
        if not strainer:
            the_page = bs(response.read(), 'html.parser')
        else:
            the_page = bs(response.read(), 'html.parser', parse_only=strainer)

    if to_print:
        print(the_page.prettify())

    return the_page


def make_tag(conjugates):
    d = {'present': '-', 'preterit': '-', 'imperfect': '-', 'conditional': '-',
         'future': '-'}
    for el in conjugates:
        if 'conj-irregular' in str(el) and 'Indicative' in str(el):
            for k in d:
                if k in el['data-tense']:
                    d[k] = 'x'
                    break

    tag = ''.join(d.values())
    for k, v in d.items():
        if v != '-':
            break
    else:
        tag = 'reg'

    return tag


def inp_trans_type_tag(word, to_print=False):
    url = 'http://www.spanishdict.com/translation/'
    page = create_page(word, url, to_print)
    if len(page.find_all('div', id="translate-en")) == 0:
        pass
    else:
        only_from_spanish = SoupStrainer(id='translate-en')
        page = create_page(word, url, to_print, strainer=only_from_spanish)

    inp = page.h1.text
    translation = page.find_all('div', class_="el")[0].text
    type_ = page.find_all('div', class_="dictionary-neodict-indent-1")[
        0].previous_element
    if 'verb' in type_ and 'adverb' not in type_:
        url = 'http://www.spanishdict.com/conjugate/'
        page = create_page(word, url, to_print)
        conjugates = page.find_all('div', class_="vtable-word-text")
        tag = make_tag(conjugates)

        return inp, translation, tag, type_
    return inp, translation, '-', type_


def create_file(inpt):
    with open('output.txt', 'w', encoding='utf-8') as files:
        for el in inpt:
            s = ';'.join(prepositions(el))
            files.write(s)
            files.write('\n')


def spanish_chars(word):
    d = {'a': 225, 'e': 233, 'i': 237, 'o': 243, 'u': 250, 'n': 241}

    def char_inds(word, ch):
        return [i for i in range(len(word)) if word[i] == ch]

    if '.' in word:
        inds = [i - 1 for i in char_inds(word, '.')]
        l = list(word)
        for el in inds:
            try:
                l[el] = chr(d[word[el]])
            except KeyError:
                pass
        word = ''.join(l)
        word = word.replace('.', '')

    return word


def read_file(data):
    with open(data) as files:
        for el in files:
            yield el


def prepositions(line):
    word, trans, tag, type_ = line
    if 'noun' in str(type_):
        if 'masculine' in str(type_):
            word = 'el ' + word
        else:
            word = 'la ' + word
        trans = 'the ' + trans

    return word, trans, tag


def main():
    inpt = list()
    for word in read_file('input.txt'):
        print(word)
        word = spanish_chars(word)
        try:
            inp = inp_trans_type_tag(word, to_print=False)
            inpt.append(inp)
        except Exception as e:
            with open('error.txt', 'a') as files:
                files.write(f'Word: {word}; Error: {e}')
                files.write('\n')
    create_file(inpt)


if __name__ == '__main__':
    main()
