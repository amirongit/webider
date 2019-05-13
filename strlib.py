from random import choice
from string import ascii_lowercase
from bs4 import BeautifulSoup

def random_domain(length, *args):

    """provides random domain names."""

    domain = str()
    for i in range(length): domain += choice(list(ascii_lowercase))
    return domain + '.' + choice(list(args))

def get_domain(string):

    """gets the domains of an html web page."""

    tmpobj = BeautifulSoup(string, 'html.parser')
    links = [i.attrs['href'] for i in htm.find_all('a')]
    domains = list()
    for i in links:
        if 'http' in i:
            domain.append(i.split('/')[2])
    return domain
