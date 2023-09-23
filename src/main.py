import json
import logging
import os
import queue
from threading import Thread

from __main__ import __file__

from domain_repository import DomainRepository
from domain_service import DomainService

with open(f'{"/".join(__file__.split("/")[:-1])}/config.json') as cf:
    CONFIGURATION: dict = json.loads(cf.read())


def main() -> None:
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s - %(threadName)s - %(levelname)s: %(message)s]')

    domain_repository = DomainRepository(CONFIGURATION['database_uri'])

    domain_service = DomainService(domain_repository)
    domain_service.NETWORK_PROXIES = CONFIGURATION.get('network_proxies')

    if (network_timeout := CONFIGURATION.get('network_timeout')) is not None:
        domain_service.NETWORK_TIMEOUT = network_timeout

    surf_queue: queue.Queue = queue.Queue()

    while True:
        [surf_queue.put(domain) for domain in domain_service.get_surfable_domains()]
        max_workers: int = min(32, os.cpu_count() + 4) - 1

        if surf_queue.empty():
            random_surfers: list[Thread] = [
                Thread(
                    target=domain_service.surf_random_domains,
                    args=(2,)
                ) for _ in range(max_workers)
            ]
            [random_surfer.start() for random_surfer in random_surfers]
            [random_surfer.join() for random_surfer in random_surfers]
        else:
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
    print('''
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
    ''')
    main()
