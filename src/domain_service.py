import logging

from queue import Queue, Empty
from random import choice, randint
from sqlite3 import IntegrityError
from string import ascii_lowercase
from threading import current_thread
from typing import NoReturn, Optional

import bs4
import requests

import utils

from dto import DomainDTO, DomainQueryDTO
from domain_repository import DomainRepository


class DomainService(metaclass=utils.Singleton):
    NETWORK_TIMEOUT: int = 3
    NETWORK_PROXIES: Optional[dict[str, str]] = None

    def __init__(self, domain_repository: DomainRepository) -> NoReturn: self.domain_repository = domain_repository

    def publish_to_domain_queue(self, queue: Queue[DomainDTO]) -> NoReturn:
        while True:
            if queue.empty():
                [queue.put(domain) for domain in self.get_surfable_domains()]

    def subscribe_to_domain_queue(self, queue: Queue[DomainDTO]) -> NoReturn:
        while True:
            try:
                domain: DomainDTO = queue.get(timeout=1)
                surf_result: bool = self.surf_domain(domain)
                logging.info(
                    f'''{current_thread().name}: surfing {domain.url}: {'done' if surf_result else 'failed'}'''
                )
            except Empty:
                break

    def get_surfable_domains(self) -> list[DomainDTO]: return self.domain_repository.get(DomainQueryDTO(surfed=False))

    def surf_random_domains(self, number_of_required_domains: int) -> NoReturn:
        while number_of_required_domains > 0:
            if self.surf_domain(DomainDTO(url=self.generate_url())):
                number_of_required_domains -= 1

    def surf_domain(self, domain: DomainDTO) -> bool:
        try:
            self._surf_domain(domain)
            return True
        except (IOError, OSError, IntegrityError):
            return False

    def _surf_domain(self, domain: DomainDTO) -> NoReturn:
        response: requests.Response = requests.get(
            f'http://{domain.url}',
            proxies=self.NETWORK_PROXIES,
            timeout=self.NETWORK_TIMEOUT
        )
        if response.status_code == 200:
            domain.surfed = True
            self.domain_repository.create_or_update(domain)
            for url in self.extract_urls(response.text):
                self.domain_repository.create(DomainDTO(url=url))

    @staticmethod
    def extract_urls(plain_html: str) -> list[str]:
        vanilla_bs4: bs4.BeautifulSoup = bs4.BeautifulSoup(plain_html, 'html.parser')
        urls: list[str] = list()

        a: bs4.Tag
        for a in vanilla_bs4.find_all('a'):
            href: Optional[str] = a.attrs.get('href')
            if href is not None and 'http' in href:
                urls.append(href.split('/')[2].replace('www.', ''))

        return list(set(urls))

    @staticmethod
    def generate_url() -> str:
        url: str = str()
        for _ in range(0, randint(3, 16)):
            url += choice(list(ascii_lowercase))
        return url + '.' + choice(['com', 'org', 'net', 'biz', 'info'])
