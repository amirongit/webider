from random import choice, randint
from sqlite3 import IntegrityError
from string import ascii_lowercase
from typing import NoReturn

import bs4
import requests

import utils

from domain_repository import DomainRepository


class DomainService(metaclass=utils.Singleton):
    def __int__(self, domain_repository: DomainRepository) -> NoReturn: self.domain_repository = domain_repository

    def surf_random_domains(self, number_of_required_domains: int) -> NoReturn:
        while number_of_required_domains > 0:
            if self.surf_domain(self.generate_domain()):
                number_of_required_domains -= 1

    def surf_domain(self, domain: str, proxies: list[dict[str, str]] = None) -> bool:
        try:
            self._surf_domain(domain, proxies)
            return True
        except(IOError, OSError, IntegrityError):
            return False

    def _surf_domain(self, domain: str, proxies: list[dict[str, str]] = None) -> NoReturn:
        response: requests.Response
        if (response := requests.get(domain, proxies=proxies)).status_code == 200:
            [self.domain_repository.create_domain(url) for url in self.extract_domains(response.text)]

    @staticmethod
    def extract_domains(plain_html: str) -> list[str]:
        vanilla_bs4: bs4.BeautifulSoup = bs4.BeautifulSoup(plain_html, 'html.parser')
        urls: list[str] = list()

        a: bs4.Tag
        for a in vanilla_bs4.find_all('a'):
            href: str
            if 'http' in (href := a.attrs['href']):
                urls.append(href.split('/')[2])

        return list(set(urls))

    @staticmethod
    def generate_domain() -> str:
        url: str = str()
        for _ in range(2, randint(8, 32)):
            url += choice(list(ascii_lowercase))
        return url + '.' + choice(['com', 'org', 'net', 'biz', 'info'])
