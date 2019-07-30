from random import choice, randint
from string import ascii_lowercase
from bs4 import BeautifulSoup


class WebPage(object):
    
    def __init__(self, html_str):
        
        self.HTML_STRING = html_str

    def get_domains(self):

        "returns urls of the given HTML string!"

        tmpobj = BeautifulSoup(self.HTML_STRING, 'html.parser')
        
        urls = list()

        for url in tmpobj.find_all('a'):
            
            try:
                
                urls.append(url.attrs['href'])
            except:
                
                pass
        
        domain_names = list()

        for url in urls:
            
            if 'http' in url: 

                domain_names.append(url.split('/')[0] + '//' + url.split('/')[2])
        
        return domain_names

    def __repr__(self):

        return str(self.HTML_STRING)


def generate(*args, max_length=8):

    "generates random domain names."

    domain = str()
    while len(domain) < randint(3, max_length):

        domain += choice(list(ascii_lowercase))

    return 'http://' + domain + '.' + choice(list(args))
    
