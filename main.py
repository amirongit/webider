import datalib, domainlib, surflib
from json import load, dump
from pyfiglet import figlet_format
from subprocess import call

print(figlet_format('w3b1der'))
print('git: https://github.com/bigAmir/webider')

def start():

    "configures the config file; you can do it your self!"

    cfg = load(open('config.json'))

    if cfg['first_run']:
        tmp = input('(you can leave it empty)\nproxy: ')
        cfg['proxies']['http'] = tmp
        cfg['proxies']['https'] = tmp
        cfg['first_run'] = False
        conn = datalib.generate()
        dump(cfg, open('config.json', 'w'))

    else:
        conn = datalib.generate()

    return {'connection': conn, 'config': cfg}

def main():
    var = start()
    call('clear', shell=True)
    print(figlet_format('w3b1der'))
    opt = int(input('1 - randomly create some domains!\n2 - look in the saved urls for new domains\nany other numbers - exit!\nyour choice: '))
    
    if opt == 1: print(var); surflib.random_surf(var['connection'], var['config']['proxies'])
    if opt == 2: surflib.surf_the_data(var['connection'])
    if opt != 1 or opt != 2: exit()

if __name__ == '__main__':
    main()
