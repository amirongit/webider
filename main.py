import datalib, domainlib
from json import load, dump
from pyfiglet import figlet_format
from requests import get
from random import randint

print(figlet_format('w3b1der'))
print('git: https://github.com/bigAmir/webider')

def start(ConfigFile):
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

def random_surf(conn, proxy):
    cursor = conn.cursor()
    while True:
        tmp = domainlib.generate('com', 'ir', 'org', 'info', 'io', 'pro')
        print(tmp)
        try:
            res = get(tmp, proxies=proxy)
            if res.ok == True:
                datalib.write(tmp, cursor)
                conn.commit()
                print(tmp)
        except:
            pass




crawler = start('config.json')
random_surf(crawler['connection'], crawler['proxies'])
