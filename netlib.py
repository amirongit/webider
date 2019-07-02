from requests import get

class crawler(object):

    "it's the crawler; requests to the server and gets the content!"

    def __init__(self, proxy):
        self.proxies = proxy

    def is_ok(self, domain):

        "checks if it can access to the server or not!"

        res = get(domain, proxies=self.proxies)
        if str(res) == '<Response [200]>':

            return True
        else:

            return False

    def get(self, domain):

        "just a re-define of the get method!"

        return get(domain, proxies=self.proxies)
