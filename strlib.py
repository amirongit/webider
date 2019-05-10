from random import choice
from string import ascii_lowercase

def random_domain(length, **kwargs):

    """provides random domain names."""

    domain = str()
    for i in range(length): domain += choice(list(ascii_lowercase))
    return domain + '.' + choice(kwargs['domains'])

def get_domain_str(string):
    pass
