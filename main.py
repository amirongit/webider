from libs import stringLib, ormLib
from json import dump, load
from requests import get
from subprocess import call
from pyfiglet import figlet_format
from time import sleep
from os.path import dirname, abspath

print(figlet_format('w3b1d3r'))
print('source code: https://gitlab.com/bigAmir/webider')
sleep(2)
call('clear', shell=True)

abs_path = dirname(abspath(__file__))
with open('cfg/settings.json') as config_file: cfg = load(config_file)

def setup():

    print('running setup...')
    global cfg

    proxy = input('(leave empty if you don\'t have one!)\nexample: sokcs5h://127.0.0.1:9050\nproxy: ')

    cfg['proxies']['https'] = proxy
    cfg['proxies']['http'] = proxy
    cfg['first_run'] = False
    
    with open('cfg/settings.json', 'w+') as config_file:

        dump(cfg, config_file)

main_conn = 'this variable is going to be recreated!'
main_id_keeper = int()
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
                    data_base_connection = ormLib.create_data_base(abs_path)
                    break

        else:

            res = get(starting_domain)
            if res.status_code == 200:

                domain_pool.append(starting_domain)
                data_base_connection = ormLib.create_data_base(abs_path)

    else:

        data_base_connection = ormLib.create_data_base(abs_path)

    data_base_cursor = data_base_connection.cursor()
    
    global main_conn
    main_conn = data_base_connection

    try:

        for domain in domain_pool: ormLib.insert_new_domain(data_base_cursor, domain)
    
    except:

        pass

    domain_pool = dict()
    for Id, domain in ormLib.get_all_domains(data_base_cursor): domain_pool[Id] = domain
    
    for record in domain_pool.items():
        
        res = get(record[1], proxies=cfg['proxies'])
        
        global main_id_keeper
        main_id_keeper = record[0]

        tmp_page = stringLib.WebPage(res.text)
        tmp_domain_list = tmp_page.get_domains()

        for domain in tmp_domain_list: ormLib.insert_new_domain(data_base_cursor, domain)


if __name__ == '__main__':
    print(cfg)
    if cfg['first_run'] == True:

        setup()

        try:

            main(True)
        except (KeyboardInterrupt, SystemExit):

            with open('cfg/settings.json', 'w+') as config_file: 
                
                cfg = load(config_file)
                cfg['last_surfed_id'] = main_id_keeper
                dump(cfg, config_file)
                main_conn.commit()

                print('saving the data...')
                exit()


    else:

        try:

            main()
        except (KeyboardInterrupt, SystemExit):

            with open('cfg/settings.json', 'w+') as config_file:

                cfg = load(config_file)
                cfg['last_surfed_id'] = main_id_keeper
                dump(cfg, config_file)
                main_conn.commit()

                print('saving the data...')
                exit()
