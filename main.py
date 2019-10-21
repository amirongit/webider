from libs import stringLib, ormLib
from json import dump, load
from requests import get
from subprocess import call
from pyfiglet import figlet_format
from time import sleep

print(figlet_format('w3b1d3r'))
print('source code: https://gitlab.com/bigAmir/webider')
sleep(2)
call('clear', shell=True)

with open('cfg/settings.json') as config_file: cfg = load(config_file)

def setup(config):

    print('running setup...')
    config['first_run'] = False

    proxy = input('(leave empty if you don\'t have one!)\nexample: sokcs5://127.0.0.1:9050\nproxy: ')

    config['proxies']['https'] = proxy
    config['proxies']['http'] = proxy

    global cfg
    with open('cfg/settings.json', 'x') as config_file:

        dump(config, config_file)
        cfg = load(config_file)


def main(first_run=False):

    domain_pool = list()
    if first_run == True:

        print('at the first we need a webpage to create our domain pool!\nif you have one, enter it; if you don\'t have a url to start with, you can type \'random\' to generate a random domain!')
        starting_domain = input('\nstarting url: ')

        if starting_domain == 'random':

            while True:

                starting_domain = stringLib.generate('ir', 'com', 'org', 'net', 'us', 'uk', 'tk')
                res = get(starting_domain)
                if res.status_code == 200:

                    domain_pool.append(starting_domain)
                    data_base_connection = ormLib.create_data_base()
                    break

        else:

            res = get(starting_domain)
            if res.status_code == 200:

                domain_pool.append(starting_domain)
                data_base_connection = ormLib.create_data_base()

    else:

        data_base_connection = ormLib.create_data_base()

    data_base_cursor = data_base_connection.cursor()

    try:

        for domain in domain_pool: ormLib.insert_new_domain(data_base_cursor, domain)
    
    except:

        pass

    domain_pool = dict()
    for ID, domain in ormLib.get_all_domains(data_base_cursor): domain_pool[ID] = domain

    for record in domain_pool:

        res = get(record[1])
        id_keeper = record[0]
        tmp_page = stringLib.WebPage(res.text)
        tmp_domain_list = tmp_page.get_domains()

        for domain in tmp_domain_list: ormLib.insert_new_domain(data_base_cursor, domain)


if __name__ == 'main':

    if cfg['first_run'] == True:

        setup()
        main(True)

    else:

        main()

    # write interupt statement
