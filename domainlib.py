from random import choice, randint
from string import ascii_lowercase
from bs4 import BeautifulSoup

def random_domain(*args, length=randint(3, 10)):

    "provides random domain names."

    domain = str()
    
    while len(domain) < length: domain += choice(list(ascii_lowercase))
    
    return domain + '.' + choice(list(args))

def find_domain(html_str):

    "gets the domains of an html web page."

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
