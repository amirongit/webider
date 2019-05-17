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
    settings['settings']['proxies']['http'] = str(input('http protocol <socks5h://host:port>\nproxy: '))
    print('\n- + - + - + - + - + - + - + - + - + - + - + - +\n')
    settings['settings']['proxies']['https'] = str(input('https protocol <socks5h://host:port>\nproxy: '))
    
    settings['first_run'] = False
    json.dump(settings, open('setting.json', 'w'))
    settings = json.load(open('setting.json'))
    
    db_con = sqlite3.connect('webider.db')
    db_con.execute('CREATE TABLE domains(domain text)')
    db_con.commit()

    starting_point = str(input('random domain to start <https://exam.ple>\nurl: '))
    
    db_con.execute('INSERT INTO domains VALUES ("{}")'.format(starting_point))
    db_con.commit()
    db_con.close()

def main():
    web_crowler = session()
    tmp_db_con = sqlite3.connect('webider.db')

    while True:
        for i in tmp_db_con.execute('SELECT * FROM domains'):
            res = web_crowler.get(i[0], proxies=settings['settings']['proxies'])
            for j in domainlib.find_domain(res.text):
                tmp_db_con.execute('INSERT INTO domains VALUES ("{}")'.format(j))
                tmp_db_con.commit()

try:
    opt = int(input('\n1-veiw domains.\n2-surf!\n:'))
    if opt == 2:
        main()
    if opt == 1:
        db_con = sqlite3.connect('webider.db')
        for i in db_con.execute('SELECT * FROM domains'):
            print(i)
    else:
        print('--BAD OPTION--')
except:
    print('--BAD OPTION--')