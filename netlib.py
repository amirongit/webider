from requests import session

class crawler(session):

    def is_ok(self, domain, proxy):

        "checks if it can access to the server or not!"

        res = self.get(domain, proxies=proxy)
        if str(res) == '<Response [200]>':

            return True
        else:

            return False
