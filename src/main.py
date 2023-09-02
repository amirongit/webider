from __main__ import __file__

from threading import Thread

import json
import logging
import os
import queue

from domain_repository import DomainRepository
from domain_service import DomainService


with open(f'{"/".join(__file__.split("/")[:-1])}/config.json') as cf:
    CONFIGURATION: dict = json.loads(cf.read())


def main():
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s - %(threadName)s - %(levelname)s: %(message)s]')

    domain_repository = DomainRepository(CONFIGURATION['database_uri'])

    domain_service = DomainService(domain_repository)
    domain_service.NETWORK_PROXIES = CONFIGURATION.get('network_proxies')

    if (network_timeout := CONFIGURATION.get('network_timeout')) is not None:
        domain_service.NETWORK_TIMEOUT = network_timeout

    surf_queue: queue.Queue = queue.Queue()

    while True:
        [surf_queue.put(domain) for domain in domain_service.get_surfable_domains()]

        if surf_queue.empty():
            domain_service.surf_random_domains(16)
        else:
            max_workers: int = min(32, os.cpu_count() + 4) - 1
            publisher: Thread = Thread(target=domain_service.publish_to_domain_queue, args=(surf_queue,))
            subscribers: list[Thread] = [
                Thread(
                    target=domain_service.subscribe_to_domain_queue,
                    args=(surf_queue,)
                ) for _ in range(max_workers)
            ]

            publisher.start()
            [subscriber.start() for subscriber in subscribers]

            publisher.join()
            [subscriber.join() for subscriber in subscribers]


if __name__ == '__main__':
    main()
