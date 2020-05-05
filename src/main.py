from json import dump, load
from os.path import dirname, abspath
from requests import get
from requests.exceptions import ConnectionError, ConnectTimeout
from random import randint, choice
from socket import gaierror
from string import ascii_lowercase
from subprocess import call
from urllib3.exceptions import NewConnectionError

from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Integer, Column, String, Boolean
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

ABS_PATH = dirname(abspath(__name__))
alchemy_base = declarative_base()
alchemy_engine = create_engine(f'sqlite:///{ABS_PATH}/webider.sql')
alchemy_sessionmaker = sessionmaker(bind=alchemy_engine)
session = alchemy_sessionmaker()


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
        href = a_tag.attrs['href']
        if 'http' in href:
            urls.append(href.split('/')[2])
    return list(set(urls))


def generate_url(min_length=3, max_length=10, domain_names='com,net,org'):
    url = str()
    for i in range(randint(min_length, max_length)):
        url += choice(list(ascii_lowercase))
    url += '.' + choice(list(domain_names.split(',')))
    return url


def main():
    config = load(open(f'{ABS_PATH}/config.json'))
    if config['use_random_urls']:
        while True:
            url = generate_url()
            try:
                response = get(f'http://{url}', proxies=config['proxy'])
            except(gaierror, ConnectTimeout, ConnectionError):
                continue
            if response.status_code == 200:
                new_domain = DomainModel(url=url, surfed=False)
                if config['verbos']:
                    print('    ' + url)
                try:
                    session.add(new_domain)
                    session.commit()
                except IntegrityError:
                    session.rollback()
    else:
        while True:
            domain_pool = session.query(DomainModel).filter(
                            DomainModel.surfed == 0).all()
            for domain in domain_pool:
                try:
                    response = get(f'http://{domain.url}',
                                   proxies=config['proxy'])
                    extracted_urls = get_urls(response.text)
                    domain.surfed = True
                    session.commit()
                    for url in extracted_urls:
                        new_domain = DomainModel(url=url, surfed=False)
                        if config['verbos']:
                            print('    ' + url)
                        try:
                            session.add(new_domain)
                            session.commit()
                        except IntegrityError:
                            session.rollback()
                except(gaierror, ConnectTimeout, ConnectionError):
                    continue


if __name__ == '__main__':
    call('clear', shell=True)
    _ = input('''
                      ::
                     +ooo+
                    +oooooo:
           /++/     :ooooooo+
         :yyyyyy/     +ooooooo:
         +yyyyyyo      /ooooooo/
          /syyy+ :/+:    +oooooo+
                +ooooo+/  /oooooo+
       :       +ooooooooo+/:+ooooo+
     +ooo+:    :ooooooooooooooooooo:
    +ooooooo/    +oooo+/+ooooooooo/
    :+oooooooo+:  +oooo+  :+oooo/
      :/ooooooooo/:/ooooo:   ::
         :+oooooooo+oooooo:
            /+oooooooooooo:
               /+ooooooo+
                  :/++/


    -Source Code
    Git Repository: https://gitlab.com/bigAmir/webider

    *Configuration
    You can edit webider/config.json manually

    -Note
    To view your collected urls see webider/webider.sql
    you can use sqlitebrowser or the cli interface

    -Press Return to continue...
    ''')
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print('you can star me in gitlab if you found me useful, bye.')
            exit()
