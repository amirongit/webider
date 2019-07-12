from random import choice, randint
from string import ascii_lowercase
from bs4 import BeautifulSoup

def generate(*args):

    "generates random domains with the domain names given!"

    domain = str()
    while len(domain) < randint(3, 10): domain += choice(list(ascii_lowercase))

    return 'http://' + domain + '.' + choice(list(args))

def surf(html_str):

    "returns web page urls of the given HTML string!"

    tmpobj = BeautifulSoup(html_str, 'html.parser')
    links = list()
    for i in tmpobj.find_all('a'):
            try:
                links.append(i.attrs['href'])
            except:
                pass
    domains = list()
    for i in links:
        if 'http' in i:
            domains.append(i.split('/')[0] + '//' + i.split('/')[2])
            
    return domains
