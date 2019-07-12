import datalib, domainlib
from json import load, dump
from pyfiglet import figlet_format

print(figlet_format('w3b1der'))
print('git: https://github.com/bigAmir/webider')

def start(ConfigFile):

    "configures the config file; you can do it your self!"

    cfg = load(open(ConfigFile))

    if cfg['first_run']:
        tmp = input('(you can leave it empty)\nproxy: ')
        cfg['proxies']['http'] = tmp
        cfg['proxies']['https'] = tmp
        cfg['first_run'] = False
        conn = datalib.generate()
        dump(cfg, open(ConfigFile, 'w'))

    else:
        conn = datalib.generate()

    return {'connection': conn, 'config': cfg}


