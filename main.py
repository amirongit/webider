from json import dump, load
from os.path import dirname, abspath
from requests import get
from random import randint, choice
from string import ascii_lowercase

from sqlalchemy import create_engine, Integer, Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from bs4 import BeautifulSoup

ABS_PATH = dirname(abspath(__name__))
alchemy_base = declarative_base()
alchemy_engine = create_engine(f'sqlite:///{ABS_PATH}/webider.sql')


class DomainModel(alchemy_base):
    __tablename__ = 'domains'
    id_ = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    surfed = Column(Boolean, default=False)

    def __repr__(self):
        return f'{self.id_}: {self.url}'


alchemy_base.metadata.create_all(alchemy_engine)


def get_urls(plain_html):
    vanilla_bs4 = BeautifulSoup(plain_html, 'html.parser')
    urls = list()
    for a_tag in vanilla_bs4.find_all('a'):
        urls.append(a_tag.attrs['href'])
    return list(filter(lambda s: True if 'http' in s else False, urls))


def generate_url(min_length=3, max_length=10, domain_names='com,net,org'):
    url = str()
    for i in rang(randint(min_length, max_length)):
        url += choice(list(ascii_lowercase))
    url += '.' + choice(list(domain_names.split(',')))
    return url
