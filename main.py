import datalib, domainlib
from json import load, dump
from pyfiglet import figlet_format
from requests import get
from random import randint

print(figlet_format('w3b1der'))
print('git: https://github.com/bigAmir/webider')

def start(ConfigFile):

    "creates a connection and a cursor!"

    cfg = load(open(ConfigFile))
    if cfg['first_run']:
        tmp = input('(you can leave it empty)\nproxy: ')
        cfg['proxies']['http'] = tmp
        cfg['proxies']['https'] = tmp
        cfg['first_run'] = False
        conn = datalib.generate('webider.db')
        dump(cfg, open(ConfigFile, 'w'))
        
    else:
        conn = datalib.generate('webider.db')
        
    c = conn.cursor()

    return {'cursor': c, 'connection': conn, 'config': cfg}

def run(conn):

    cursor = conn.cursor()
    number_of_domains = datalib.get_max(cursor, 'domains')
    if number_of_domains == (None,):
        while True:
            tmp = 'https://aparat.com'
            print(tmp)
            res = get(tmp)
            if res.ok == True:
                datalib.write(tmp, cursor)
                conn.commit()
                print('done.')
    else:
        i = datalib.read(2, cursor)
        print(i)

crawler = start('config.json')
run(crawler['connection'])