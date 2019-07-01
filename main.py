import datalib, domainlib
from sqlite3 import connect
from json import load, dump
from pyfiglet import figlet_format
from requests import session
from os import getcwd

### intro!
print(figlet_format('w3b1d3r'))
print('info: https://github.com/bigAmir/webider')

def wizard_config():

    try:
        cfg = load(open('config.json'))
    except:
        print('missing config file!')
        exit()
    
    """does the configiration in the first run.(you can do it manually!)"""

    if cfg['first_run'] == True:
        ### you can leave it empty!
        cfg['proxies']['http'], cfg['proxies']['https'] = input('proxy: ')
        conn = datalib.generate('webider.db')
        cfg['first_run'] = False
        dump(cfg, 'config.json')

    else:
        conn = connect('webider.db')

    c = conn.cursor()


