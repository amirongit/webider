from random import choice
from string import ascii_lowercase

def mk_domaim(length, **kwargs):

    ### - at the beginning of the job, we don't know where to start from; so I just randomly make some domains to
    ### - go there and get other domains!

    """provides random domain names."""

    domain = str()
    for i in range(length): domain += choice(list(ascii_lowercase))
    return domain + '.' + choice(kwargs['domains'])
