"""the main document; run this file by python to start the actual program!"""

from json import dump, load
from atexit import register
from os.path import dirname, abspath
from time import sleep
from subprocess import call
from requests import get
from pyfiglet import figlet_format
from libs import string_lib, orm_lib

print(figlet_format('w3b1d3r'))
print('source code: https://gitlab.com/bigAmir/webider')
sleep(2)
call('clear', shell=True)

_ABS_PATH = dirname(abspath(__file__))

with open('cfg/settings.json') as config_file:

    CFG = load(config_file)

def setup():

    """this function does the setup process and configures the settings.json file."""

    print('running setup...')
    global CFG

    proxy = input('(leave empty if you don\'t have one!)\nexample: sokcs5h://127.0.0.1:9050\nproxy: ')

    CFG['proxies']['https'] = proxy
    CFG['proxies']['http'] = proxy
    CFG['first_run'] = False

    with open('cfg/settings.json', 'w+') as config_file:

        dump(CFG, config_file)

MAIN_CONN = 'this variable is going to be re-difined!'
MAIN_ID_KEEPER = int()

def main(first_run=False):

    """the main function of the program; this is what I was coding for!"""

    domain_pool = list()

    if first_run:

        print('at the first we need a webpage to create our domain pool!\nif you have one, enter it; if you don\'t have a url to start with, you can type \'random\' to generate a random domain!')
        starting_domain = input('\nstarting url: ')

        if starting_domain == 'random':

            while True:

                starting_domain = string_lib.generate('ir', 'com', 'org', 'net', 'us', 'uk', 'tk')
                print(starting_domain)
                res = get(starting_domain)

                if res.status_code == 200:

                    domain_pool.append(starting_domain)
                    data_base_connection = orm_lib.create_data_base(_ABS_PATH)
                    break

        else:

            res = get(starting_domain)
            if res.status_code == 200:

                domain_pool.append(starting_domain)
                data_base_connection = orm_lib.create_data_base(_ABS_PATH)

    else: data_base_connection = orm_lib.create_data_base(_ABS_PATH)

    data_base_cursor = data_base_connection.cursor()
    orm_lib.insert_new_domain(data_base_cursor, starting_domain)

    global MAIN_CONN
    MAIN_CONN = data_base_connection

    try:

        for domain in domain_pool:

            orm_lib.insert_new_domain(data_base_cursor, domain)

    except:

        pass

    domain_pool = dict()

    while True:

        for i_d, domain in orm_lib.get_all_domains(data_base_cursor, CFG['last_surfed_id']):

            domain_pool[i_d] = domain

        for record in domain_pool.items():

            res = get(record[1], proxies=CFG['proxies'])

            global MAIN_ID_KEEPER
            MAIN_ID_KEEPER = record[0]

            tmp_page = string_lib.WebPage(res.text)
            tmp_domain_list = tmp_page.get_domains()

            for domain in tmp_domain_list:

                print(domain)

                try:

                    orm_lib.insert_new_domain(data_base_cursor, domain)

                except:

                    pass

@register
def commit_and_exit():

    """this function will be called when the program stops working;
    it saves the data base changes and dumps the last surfed id to
    the settings.json file."""

    global MAIN_ID_KEEPER
    global MAIN_CONN

    cfg = load(open('cfg/settings.json'))
    cfg['last_surfed_id'] = MAIN_ID_KEEPER
    dump(cfg, open('cfg/settings.json', 'w+'))

    MAIN_CONN.commit()

if __name__ == '__main__':

    if CFG['first_run']:

        setup()
        main(True)

    else:

        main()
