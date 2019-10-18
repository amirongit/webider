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


def main():
    pass


if __name__ == 'main':
    
    if cfg['first_run'] == True:
        
        setup()

    main()
