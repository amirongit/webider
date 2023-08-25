from __main__ import __file__

import json
import queue
import threading

from domain_repository import DomainRepository
from domain_service import DomainService


with open(f'{"/".join(__file__.split("/")[:-1])}/config.json') as cf:
    CONFIGURATION: dict = json.loads(cf.read())


def main():
    domain_repository = DomainRepository(CONFIGURATION['database_uri'])

    domain_service = DomainService(domain_repository)
    domain_service.NETWORK_PROXIES = CONFIGURATION['network_proxies']
    domain_service.NETWORK_TIMEOUT = CONFIGURATION['network_timeout']

    surf_queue: queue.Queue = queue.Queue()

    while True:
        [surf_queue.put(domain) for domain in domain_service.get_surfable_domains()]
        if surf_queue.empty():
            domain_service.surf_random_domains(16)
        else:
            pass


if __name__ == '__main__':
    print(CONFIGURATION)
