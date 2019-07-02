from requests import session

class crawler(session):

    def is_ok(domain, proxies={}):

        "checks if it can access to the server or not!"

        res = self.get(domain, proxies=proxies)
        if str(res) == '<Response [200]>':

            return True
        else:

            return False
