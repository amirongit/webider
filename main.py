import domainlib

import sqlite3
import json

from pyfiglet import figlet_format
from requests import session

print(figlet_format('webider'))
print('https://github.com/bigAmir')

settings = json.load(open('setting.json'))

if settings['first_run']:
    
    print('first time running, pls spend 20 seconds to config webider!')
    
    print('\n- + - + - + - + - + - + - + - + - + - + - + - +\n')
    settings['settings']['proxies']['http'] = str(input('http protocol <host:port>\nproxy: '))
    print('\n- + - + - + - + - + - + - + - + - + - + - + - +\n')
    settings['settings']['proxies']['https'] = str(input('https protocol <host:port>\nproxy: '))
    
    settings['first_run'] = False
    json.dump(settings, open('setting.json', 'w'))
    settings = json.load(open('setting.json'))
    
    db_con = sqlite3.connect('webider.db')
    db_con.execute('CREATE TABLE domains(domain text)')
    db_con.commit()

    starting_point = str(input('random domain to start <https://exam.ple>\n'))
    
    db_con.execute('INSERT INTO domains VALUES ("{}")'.format(starting_point))
    db_con.commit()
    db_con.close()
